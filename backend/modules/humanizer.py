# backend/app/modules/humanizer.py
"""
Módulo de Humanización - VERSIÓN MEJORADA
Fixes aplicados:
- P0-1: Batch async con asyncio.gather
- P0-2: Validación overlap mejorada con key terms
- P0-3: Cache LRU en memoria
- P1-1: Humanness score calculator
- P1-2: Temperatura dinámica por técnica
- P1-3: Refusal patterns ampliados
"""

import re
import random
import asyncio
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from functools import lru_cache

import structlog

from backend.core.base_module import BaseModule

logger = structlog.get_logger(module="humanizer")


class Humanizer(BaseModule):
    """
    Módulo de Humanización
    
    Transforma contenido para que suene auténticamente humano.
    Sin métricas fake. Sin complicaciones innecesarias.
    """

    MODULE_ID = "humanizer"
    MODULE_NAME = "Humanizer"
    MODULE_DESCRIPTION = "Makes content sound authentically human"

    # FIX P1-3: Refusal patterns ampliados
    REFUSAL_PATTERNS = [
        "lo siento",
        "no puedo",
        "como modelo",
        "como ia",
        "como asistente",
        "no está permitido",
        "va en contra de",
        "política de uso",
        "no soy capaz",
        "mis directrices",
        "contenido inapropiado"
    ]
    
    # FIX P0-2: Stopwords para extracción key terms
    STOPWORDS = {
        "el", "la", "los", "las", "un", "una", "unos", "unas",
        "de", "del", "a", "al", "en", "con", "por", "para",
        "y", "o", "pero", "si", "no", "que", "como", "es", "son"
    }

    def __init__(self, llm_manager, config: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.llm = llm_manager
        
        config = config or {}
        # FIX P1-2: Ya no usamos temperatura fija
        self.base_temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 1500)
        
        # FIX P0-2: Thresholds mejorados
        self.min_content_ratio = config.get("min_content_ratio", 0.6)
        self.min_overlap = config.get("min_overlap", 0.5)  # NEW: 50% mínimo
        self.min_key_terms = config.get("min_key_terms", 0.7)  # NEW: 70% términos clave
        
        # FIX P0-3: Cache simple en memoria (dict)
        self._cache = {}
        self.cache_ttl = config.get("cache_ttl", 3600)  # 1 hora
        
        # Ejemplos reales de escritura humana
        self.examples = [
            "La verdad es que al principio no me convencía. Pero después... wow.",
            "¿Te ha pasado? Estás ahí, mirando la pantalla, y nada tiene sentido.",
            "No sé si es solo yo, pero cada vez que leo esto, pienso: ¿en serio?",
            "Mira, —y esto es importante— no todo tiene que ser perfecto.",
        ]

    # FIX P1-2: Temperatura dinámica por técnica
    def _get_temperature(self, techniques: List[str]) -> float:
        """Determina temperatura óptima según técnicas."""
        temps = {
            "conversational_tone": 0.7,
            "humor": 0.9,  # Más creatividad
            "professional": 0.5,  # Más conservador
            "anecdotes": 0.8,
            "emotional_triggers": 0.75,
            "vulnerability": 0.65,
            "relatability": 0.7
        }
        
        # Usar la temperatura más alta de las técnicas aplicadas
        technique_temps = [temps.get(t, self.base_temperature) for t in techniques]
        return max(technique_temps) if technique_temps else self.base_temperature

    # FIX P0-3: Cache helpers
    def _cache_key(self, text: str, techniques: List[str], voice_profile: Optional[Dict] = None) -> str:
        """Genera cache key único."""
        profile_str = str(sorted(voice_profile.items())) if voice_profile else ""
        content = f"{text}:{','.join(sorted(techniques))}:{profile_str}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """Recupera del cache si existe y no expiró."""
        if key in self._cache:
            cached_data, timestamp = self._cache[key]
            age = (datetime.now(timezone.utc) - timestamp).total_seconds()
            
            if age < self.cache_ttl:
                logger.debug("humanizer.cache_hit", key=key[:8])
                return cached_data
            else:
                # Expiró, limpiar
                del self._cache[key]
        
        return None
    
    def _set_cache(self, key: str, data: Dict[str, Any]) -> None:
        """Guarda en cache."""
        self._cache[key] = (data, datetime.now(timezone.utc))
        
        # Limpieza simple: si cache > 1000 entries, limpiar viejos
        if len(self._cache) > 1000:
            self._cleanup_cache()
    
    def _cleanup_cache(self) -> None:
        """Limpia entradas expiradas del cache."""
        now = datetime.now(timezone.utc)
        expired_keys = [
            k for k, (_, ts) in self._cache.items()
            if (now - ts).total_seconds() > self.cache_ttl
        ]
        
        for key in expired_keys:
            del self._cache[key]
        
        logger.info("humanizer.cache_cleanup", removed=len(expired_keys), remaining=len(self._cache))

    # FIX P0-2: Extracción key terms
    def _extract_key_terms(self, text: str) -> set:
        """Extrae términos clave filtrando stopwords."""
        words = text.lower().split()
        # Filtrar stopwords y palabras muy cortas
        key_words = [w for w in words if w not in self.STOPWORDS and len(w) > 2]
        return set(key_words)

    async def humanize(
        self,
        text: str,
        voice_profile: Optional[Dict[str, Any]] = None,
        techniques: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Humaniza el contenido.
        
        Args:
            text: Texto a humanizar
            voice_profile: Perfil de voz (opcional)
            techniques: Técnicas específicas (opcional)
        
        Returns:
            {
                "original": str,
                "humanized": str,
                "applied": bool,
                "humanness_score": int,  # NEW
                "reason": str (si failed)
            }
        """
        
        if not text or len(text.strip()) < 20:
            return {
                "original": text,
                "humanized": text,
                "applied": False,
                "humanness_score": 0,
                "reason": "Text too short"
            }
        
        # Determinar técnicas a aplicar
        if techniques is None:
            techniques = self._select_techniques(voice_profile)
        
        # FIX P0-3: Check cache primero
        cache_key = self._cache_key(text, techniques, voice_profile)
        cached = self._get_cache(cache_key)
        if cached:
            return cached
        
        try:
            # Humanizar con LLM
            humanized = await self._humanize_with_llm(text, voice_profile, techniques)
            
            # Validar output
            if not self._is_valid_output(text, humanized):
                raise ValueError("LLM output invalid or too short")
            
            # Post-procesamiento
            humanized = self._post_process(humanized)
            
            # FIX P1-1: Calcular humanness score
            humanness_score = self._calculate_humanness_score(humanized)
            
            logger.info(
                "humanizer.success",
                original_length=len(text),
                humanized_length=len(humanized),
                humanness_score=humanness_score
            )
            
            result = {
                "original": text,
                "humanized": humanized,
                "applied": True,
                "humanness_score": humanness_score,
                "techniques_applied": techniques
            }
            
            # FIX P0-3: Guardar en cache
            self._set_cache(cache_key, result)
            
            return result
            
        except Exception as e:
            logger.error("humanizer.failed", error=str(e))
            return {
                "original": text,
                "humanized": text,
                "applied": False,
                "humanness_score": 0,
                "reason": str(e)
            }

    def _select_techniques(self, voice_profile: Optional[Dict[str, Any]]) -> List[str]:
        """Selecciona técnicas basadas en el perfil de voz."""
        base = ["conversational_tone", "relatability"]
        
        if voice_profile:
            tone = voice_profile.get("tone", "").lower()
            
            if "casual" in tone or "friendly" in tone:
                base.extend(["humor", "anecdotes"])
            elif "professional" in tone:
                base.append("vulnerability")
            elif "inspirational" in tone:
                base.extend(["emotional_triggers", "anecdotes"])
        
        return base

    async def _humanize_with_llm(
        self,
        text: str,
        voice_profile: Optional[Dict[str, Any]],
        techniques: List[str]
    ) -> str:
        """Llama al LLM para humanizar."""
        
        tone_hint = "conversacional y auténtico"
        if voice_profile:
            tone_hint = voice_profile.get("tone", tone_hint)
        
        # FIX P1-2: Temperatura dinámica
        temperature = self._get_temperature(techniques)
        
        prompt = f"""Reescribe este texto para que suene 100% humano, no generado por IA.

Tono deseado: {tone_hint}
Técnicas a aplicar: {', '.join(techniques)}

REGLAS OBLIGATORIAS:
✅ Añade 1-2 preguntas retóricas
✅ Usa puntos suspensivos (...) para pausas naturales
✅ Incluye digresiones con guiones —así—
✅ Varía la longitud de las frases
✅ Usa palabras de relleno: "bueno", "mira", "la verdad"

❌ NO cambies el mensaje central
❌ NO inventes datos o estadísticas
❌ NO seas excesivamente formal

Ejemplo de estilo humano:
"{random.choice(self.examples)}"

Texto original:
{text}

Devuelve SOLO el texto humanizado, sin explicaciones ni comentarios.
"""

        response = await self.llm.generate_content(
            prompt,
            max_tokens=self.max_tokens,
            temperature=temperature  # FIX P1-2: Temperatura dinámica
        )
        
        # Validar respuesta
        if not isinstance(response, str) or not response.strip():
            raise ValueError("LLM returned empty or invalid response")
        
        # FIX P1-3: Detectar rechazo del LLM con patterns ampliados
        response_lower = response.lower()
        if any(pattern in response_lower for pattern in self.REFUSAL_PATTERNS):
            logger.warning("humanizer.llm_refused", response_preview=response[:100])
            raise ValueError("LLM refused to process")
        
        return response.strip()

    def _post_process(self, text: str) -> str:
        """Post-procesamiento ligero."""
        
        # Reemplazar conectores formales
        replacements = [
            (r'\bEn conclusión\b', 'Al final'),
            (r'\bPor otro lado\b', 'Pero mira'),
            (r'\bAdemás\b', 'Y encima'),
            (r'\bSin embargo\b', 'Pero'),
        ]
        
        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE, count=1)
        
        return text

    # FIX P0-2: Validación mejorada con key terms
    def _is_valid_output(self, original: str, humanized: str) -> bool:
        """Valida que el output sea usable."""
        
        if not humanized or not humanized.strip():
            return False
        
        # No debe ser demasiado corto
        ratio = len(humanized) / len(original) if len(original) > 0 else 0
        if ratio < self.min_content_ratio:
            logger.warning("humanizer.validation_failed", reason="too_short", ratio=ratio)
            return False
        
        # Validación overlap general (palabras totales)
        original_words = set(original.lower().split())
        humanized_words = set(humanized.lower().split())
        
        if not original_words:
            return False
        
        general_overlap = len(original_words & humanized_words) / len(original_words)
        
        if general_overlap < self.min_overlap:
            logger.warning("humanizer.validation_failed", reason="low_overlap", overlap=general_overlap)
            return False
        
        # FIX P0-2: Validación key terms (sin stopwords)
        original_keys = self._extract_key_terms(original)
        humanized_keys = self._extract_key_terms(humanized)
        
        if not original_keys:
            # Si no hay key terms, usar overlap general
            return general_overlap > self.min_overlap
        
        key_overlap = len(original_keys & humanized_keys) / len(original_keys)
        
        if key_overlap < self.min_key_terms:
            logger.warning(
                "humanizer.validation_failed",
                reason="low_key_terms",
                key_overlap=key_overlap,
                original_keys_count=len(original_keys),
                preserved_keys=len(original_keys & humanized_keys)
            )
            return False
        
        return True

    # FIX P1-1: Humanness score calculator
    def _calculate_humanness_score(self, text: str) -> int:
        """
        Calcula score 0-100 de qué tan humano suena el texto.
        
        Criterios:
        - Preguntas retóricas: +20
        - Puntos suspensivos: +15
        - Guiones digresión: +15
        - Palabras relleno: +20
        - Variación longitud frases: +15
        - Emojis/emoticons: +15
        """
        
        score = 0
        
        # Preguntas retóricas (+20)
        if re.search(r'\?', text):
            questions = len(re.findall(r'\?', text))
            score += min(questions * 10, 20)  # Máx 20 puntos
        
        # Puntos suspensivos (+15)
        if '...' in text:
            ellipsis = len(re.findall(r'\.{3,}', text))
            score += min(ellipsis * 8, 15)  # Máx 15 puntos
        
        # Guiones digresión (+15)
        if re.search(r'—.+?—', text):
            dashes = len(re.findall(r'—.+?—', text))
            score += min(dashes * 8, 15)  # Máx 15 puntos
        
        # Palabras relleno (+20)
        fillers = ['bueno', 'mira', 'verdad', 'pues', 'entonces', 'claro']
        text_lower = text.lower()
        filler_count = sum(1 for f in fillers if f in text_lower)
        score += min(filler_count * 5, 20)  # Máx 20 puntos
        
        # Variación longitud frases (+15)
        sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
        if len(sentences) > 1:
            lengths = [len(s.split()) for s in sentences]
            variance = max(lengths) - min(lengths)
            if variance > 5:
                score += 15
            elif variance > 3:
                score += 10
        
        # Emojis o emoticons (+15)
        if re.search(r'[😀-🙏]|:\)|:\(|:D|;-?\)', text):
            score += 15
        
        return min(score, 100)

    # ===== MÉTODOS ADICIONALES (OPCIONALES) =====
    
    async def add_anecdote(self, content: str, topic: str) -> Dict[str, Any]:
        """Añade una anécdota al contenido."""
        
        prompt = f"""Añade una anécdota breve y relevante a este contenido:

Contenido: {content}
Tema: {topic}

La anécdota debe:
- Ser de 2-3 frases máximo
- Ilustrar el punto principal
- Sonar auténtica, no inventada
- Integrarse naturalmente

Devuelve el contenido completo con la anécdota integrada.
"""
        
        try:
            enhanced = await self.llm.generate_content(prompt, max_tokens=800, temperature=0.7)
            return {"enhanced_content": enhanced, "applied": True}
        except Exception as e:
            return {"enhanced_content": content, "applied": False, "reason": str(e)}

    async def add_humor(self, content: str, humor_type: str = "subtle") -> Dict[str, Any]:
        """Añade humor al contenido."""
        
        humor_desc = {
            "subtle": "humor sutil y profesional",
            "conversational": "humor casual y amigable",
            "observational": "humor observacional sobre el tema"
        }.get(humor_type, "humor ligero")
        
        prompt = f"""Añade {humor_desc} a este contenido:

{content}

Requisitos:
- Que sea natural, no forzado
- Apropiado para el contexto
- Que refuerce el mensaje, no lo distraiga

Devuelve el contenido con humor integrado.
"""
        
        try:
            enhanced = await self.llm.generate_content(prompt, max_tokens=800, temperature=0.8)
            return {"enhanced_content": enhanced, "applied": True, "humor_type": humor_type}
        except Exception as e:
            return {"enhanced_content": content, "applied": False, "reason": str(e)}

    # FIX P0-1: Batch async con asyncio.gather
    async def humanize_batch(
        self,
        contents: List[str],
        voice_profile: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Humaniza múltiples contenidos en paralelo.
        
        MEJORA: Usa asyncio.gather para procesar concurrentemente.
        """
        
        # Crear tasks en paralelo
        tasks = [
            self.humanize(content, voice_profile)
            for content in contents
        ]
        
        # Ejecutar en paralelo, manejar excepciones
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Procesar resultados
        processed = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Si falló, devolver original
                logger.error(
                    "humanizer.batch_item_failed",
                    index=i,
                    error=str(result)
                )
                processed.append({
                    "original": contents[i],
                    "humanized": contents[i],
                    "applied": False,
                    "humanness_score": 0,
                    "reason": str(result)
                })
            else:
                processed.append(result)
        
        logger.info(
            "humanizer.batch_complete",
            total=len(contents),
            successful=sum(1 for r in processed if r.get("applied")),
            failed=sum(1 for r in processed if not r.get("applied"))
        )
        
        return processed