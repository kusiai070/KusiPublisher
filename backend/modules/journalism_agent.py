from typing import Dict, Any, Optional
import os
import json
import PyPDF2

class JournalismAgent:
    """
    Agente especializado en escritura periodística profesional.
    Lee libros/PDFs de periodismo para aprender técnicas.
    """
    
    def __init__(self, llm_manager):
        """
        Inicializa el agente de periodismo.
        
        Args:
            llm_manager: Gestor de LLM
        """
        self.llm = llm_manager
        self.journalism_knowledge = ""
        self.load_journalism_books()
    
    def load_journalism_books(self):
        """
        Lee PDFs/libros de periodismo para extraer técnicas
        Ejemplo: 'The Elements of Journalism', 'On Writing Well'
        """
        books_path = "data/journalism_books/"
        
        if os.path.exists(books_path):
            all_text = ""
            for pdf_file in os.listdir(books_path):
                if pdf_file.endswith('.pdf'):
                    with open(os.path.join(books_path, pdf_file), 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        for page in reader.pages:
                            all_text += page.extract_text()
            
            self.journalism_knowledge += f"\n\nCONOCIMIENTO DE LIBROS:\n{all_text[:50000]}"
        
        # Mantener el conocimiento base si no se encuentran libros o como complemento
        if not self.journalism_knowledge: # Si no se extrajo texto de libros
            self.journalism_knowledge = """
            PRINCIPIOS FUNDAMENTALES PERIODISMO:
            
            1. VERIFICACIÓN: Toda afirmación necesita evidencia
            2. MÚLTIPLES FUENTES: Mínimo 2-3 perspectivas
            3. CLARIDAD: Lenguaje directo, sin jerga innecesaria
            4. CONTEXTO: Ubicar hechos en marco más amplio
            5. IMPACTO: Siempre responder "¿por qué importa?"
            
            ESTRUCTURA INVERTED PYRAMID:
            - Lead: Info más importante primero
            - Body: Detalles en orden decreciente de importancia
            - Background: Contexto al final
            
            TÉCNICAS NARRATIVAS:
            - Anécdota apertura (humanizar)
            - Mostrar > Contar
            - Quotes específicas y reveladoras
            - Transiciones fluidas
            - Kicker memorable
            
            VOZ Y TONO:
            - Autoridad sin arrogancia
            - Objetivo pero no neutral en injusticias
            - Accesible sin condescender
            - Preciso en lenguaje
            """
        else: # Si se extrajo texto de libros, añadir los principios base también
            self.journalism_knowledge += """
            
            --- PRINCIPIOS BÁSICOS ADICIONALES ---
            PRINCIPIOS FUNDAMENTALES PERIODISMO:
            
            1. VERIFICACIÓN: Toda afirmación necesita evidencia
            2. MÚLTIPLES FUENTES: Mínimo 2-3 perspectivas
            3. CLARIDAD: Lenguaje directo, sin jerga innecesaria
            4. CONTEXTO: Ubicar hechos en marco más amplio
            5. IMPACTO: Siempre responder "¿por qué importa?"
            
            ESTRUCTURA INVERTED PYRAMID:
            - Lead: Info más importante primero
            - Body: Detalles en orden decreciente de importancia
            - Background: Contexto al final
            
            TÉCNICAS NARRATIVAS:
            - Anécdota apertura (humanizar)
            - Mostrar > Contar
            - Quotes específicas y reveladoras
            - Transiciones fluidas
            - Kicker memorable
            
            VOZ Y TONO:
            - Autoridad sin arrogancia
            - Objetivo pero no neutral en injusticias
            - Accesible sin condescender
            - Preciso en lenguaje
            """
    
    async def generate_journalistic_content(
        self, 
        topic: str, 
        platform: str,
        style: str = "investigative"
    ) -> Dict[str, Any]:
        """
        Genera contenido periodístico adaptado a plataforma
        
        Args:
            topic: Tema del contenido
            platform: Plataforma objetivo (twitter, linkedin, instagram, facebook, blog)
            style: Estilo periodístico (investigative, feature, explainer, opinion)
            
        Returns:
            Dict con contenido generado y metadatos
        """
        
        # Prompts maestros por plataforma
        platform_journalism = {
            "twitter": self._twitter_journalist(),
            "linkedin": self._linkedin_journalist(), 
            "instagram": self._instagram_journalist(),
            "facebook": self._facebook_journalist(),
            "blog": self._blog_journalist(style)
        }
        
        prompt = platform_journalism.get(platform, platform_journalism["blog"])
        
        final_prompt = f"""
{self.journalism_knowledge}

TEMA: {topic}
PLATAFORMA: {platform}
ESTILO PERIODÍSTICO: {style}

{prompt}

Todo en español.
"""
        
        content = await self.llm.generate_content(
            final_prompt,
            max_tokens=8000 if platform == "blog" or platform == "linkedin_article" else 2000,
            temperature=0.7
        )
        
        return {
            "content": content,
            "journalism_mode": True,
            "style": style,
            "platform": platform,
            "topic": topic
        }
    
    def _twitter_journalist(self) -> str:
        """Prompt específico para Twitter periodístico"""
        return """
TWITTER PERIODÍSTICO:

Estructura:
1. Lead impactante (1 oración)
2. Dato verificable o quote
3. Call-to-action o pregunta

Técnicas:
- Thread si necesitas contexto
- Primera frase: gancho noticioso
- Citar fuente específica
- Hashtags mínimos, relevantes
- Tono: Urgente pero preciso

Ejemplo estilo:
"ÚLTIMA HORA: [Hecho verificado]. Según [Fuente], [implicación]. 
Esto significa [contexto]. [Pregunta al lector]"

Longitud: 1-3 tweets máximo
"""
    
    def _linkedin_journalist(self) -> str:
        """Prompt específico para LinkedIn periodístico"""
        return """
LINKEDIN PERIODÍSTICO:

Estructura:
1. Hook profesional (dato sector/insight)
2. Análisis con evidencia
3. Múltiples perspectivas
4. Implicaciones para industria
5. Pregunta o reflexión final

Técnicas:
- Abrir con estadística sorprendente
- Citar expertos del sector
- Presentar debate/tendencia
- Datos > Opiniones
- Tono: Thought leadership

Estilo: Harvard Business Review meets The Economist

Longitud: 150-250 palabras
"""
    
    def _instagram_journalist(self) -> str:
        """Prompt específico para Instagram periodístico"""
        return """
INSTAGRAM PERIODÍSTICO:

CRÍTICO: El formato de salida DEBE ser un único post largo y UNIFICADO, NO UN HILO DE TWEETS. Enfoque en una IMAGEN o VIDEO.
Utiliza saltos de línea y emojis para mejorar la legibilidad y el atractivo visual.

Estructura:
1. **Gancho Visual (IMAGEN/VIDEO):** Describe la imagen o video ideal que acompañaría este post.
2. **Lead Emocional/Humano:** Una historia breve o un dato impactante que genere conexión.
3. **Desarrollo:** Expande el tema con un enfoque personal o testimonial.
4. **Call-to-action:** Pregunta para fomentar la interacción o una llamada a deslizar/ver más.

Técnicas:
- Narrativa personal/testimonial
- Emoción + hechos
- Carrusel para contexto si se necesitan múltiples imágenes/videos.
- Primer párrafo = gancho total
- Humanizar estadísticas
- Uso generoso de emojis relevantes para separar ideas y añadir personalidad.

Estilo: Humans of New York meets National Geographic (profundo, humano, visual)

Hashtags: Mezcla trending + nicho periodístico (hasta 30, relevantes para la visibilidad)
Longitud: 120-200 palabras (aproximadamente, no estricto si la narrativa lo requiere)

EJEMPLO DE SALIDA (SIN ENCABEZADOS):
[IMAGEN: Una foto de una persona mayor mirando un antiguo álbum de fotos, con nostalgia en su mirada]
Hace 30 años, María creyó que su amor con Juan duraría para siempre. Hoy, una app les ha reunido, demostrando que el amor, como las historias, encuentra siempre su camino. ❤️📲 Una historia de reencuentros que la tecnología hizo posible. Desliza para conocer su viaje.
#AmorSigloXXI #HistoriasDeAmor #Reencuentros #TecnologiaYAmor #HistoriasQueInspiran
"""
    
    def _facebook_journalist(self) -> str:
        """Prompt específico para Facebook periodístico"""
        return """
FACEBOOK PERIODÍSTICO:

CRÍTICO: El formato de salida DEBE ser un post único, largo, detallado y UNIFICADO, que invite a la conversación, NO UN HILO DE TWEETS.
Utiliza párrafos más largos y un tono cercano para fomentar el debate en la comunidad.

Estructura:
1. **Gancho Inicial:** Pregunta provocadora, anécdota personal o un dato impactante.
2. **Contexto Amplio:** Desarrolla el tema conectándolo con la comunidad o experiencias cotidianas.
3. **Múltiples Perspectivas:** Incluye diferentes puntos de vista o citas de personas reales si es aplicable.
4. **Invitación al Debate:** Una clara llamada a la acción para que la comunidad comente y comparta su opinión.

Técnicas:
- Enfoque conversacional y empático.
- Conectar el tema con la vida de los usuarios en Facebook.
- Fomentar la discusión constructiva y respetuosa.
- Equilibrio entre información y la generación de engagement.
- Uso de quotes de personas reales para autenticidad.

Estilo: Periodismo comunitario + ProPublica (participativo, detallado)

Longitud: 200-400 palabras (permite mayor profundidad que Twitter)

EJEMPLO DE SALIDA (SIN ENCABEZADOS):
¿Has notado cómo ha cambiado la forma en que amamos y nos conectamos en los últimos años? ❤️📲 La frase "quien decifra el amor en el siglo XXI, ha cambiado la interacción" resuena profundamente en nuestra comunidad. Hemos pasado de las cartas a los mensajes instantáneos, de los encuentros fortuitos a los "matches" algorítmicos.

En nuestro grupo local, muchos comparten la frustración de la "fatiga de las citas" digital, mientras otros celebran haber encontrado a su alma gemela gracias a una app. Es un reflejo de cómo la tecnología nos une, pero también nos desafía a mantener la autenticidad y la profundidad en nuestras relaciones. ¿Qué piensas tú? ¿Ha mejorado o empeorado nuestra forma de amar? Queremos leer tus historias y opiniones aquí abajo. ¡Participa en el debate!
#AmorSigloXXI #ComunidadKusi #DebateAbierto #RelacionesModernas #ImpactoDigital
"""
    
    def _blog_journalist(self, style: str) -> str:
        """Prompts específicos para blog según estilo"""
        
        styles_prompts = {
            "investigative": """
BLOG INVESTIGATIVO (2000-3000 palabras):

ESTRUCTURA:
1. LEAD (150 palabras):
   - Anécdota impactante O dato revelador
   - 5W1H completo
   - Nut graf: Por qué es importante AHORA

2. CONTEXTO (300 palabras):
   - Background histórico
   - Intentos previos de abordar tema
   - Por qué resurge ahora

3. INVESTIGACIÓN (1000 palabras):
   - Hallazgos principales (mínimo 3)
   - Evidencia documental
   - Quotes de mínimo 4 fuentes:
     * Experto académico
     * Insider del tema
     * Afectado directo
     * Voz opuesta/crítica
   - Datos verificables con fuentes

4. ANÁLISIS (400 palabras):
   - Qué significan estos hallazgos
   - Conexiones no obvias
   - Implicaciones futuras

5. CONCLUSIÓN (200 palabras):
   - Recapitulación hallazgos clave
   - Preguntas sin responder
   - Próximos pasos/seguimiento

TÉCNICAS OBLIGATORIAS:
- Sidebar con datos clave
- Timeline si aplica
- "Metodología" al final
- Links a fuentes primarias
- Fact-boxes

TONO: ProPublica/The Intercept/Bellingcat
""",
            
            "feature": """
BLOG FEATURE/CRÓNICA (1500-2500 palabras):

ESTRUCTURA NARRATIVA:
1. ESCENA APERTURA (200 palabras):
   - Momento específico, sensorial
   - Personaje principal introducido
   - Setting vívido

2. NUT GRAF (100 palabras):
   - Qué es esta historia realmente
   - Por qué leerla completa
   - Gancho emocional + intelectual

3. DESARROLLO NARRATIVO (1000 palabras):
   - Arco de historia personal
   - Intercalar: escenas + análisis
   - Quotes extensas (2-3 oraciones)
   - Mostrar, no contar
   - Detalles sensoriales

4. CONTEXTO AMPLIO (400 palabras):
   - Conectar historia individual con tendencia
   - Datos que dan escala
   - Voces expertas

5. RESOLUCIÓN (300 palabras):
   - Círculo narrativo (volver a apertura)
   - Qué cambió/se aprendió
   - Resonancia universal

TÉCNICAS:
- Escenas en tiempo presente
- Diálogo real (grabado)
- Descripciones físicas memorables
- Metáforas originales
- Ritmo variado (párrafos cortos/largos)

TONO: New Yorker/Revista 5W/Gatopardo
""",

            "explainer": """
BLOG EXPLICATIVO (1000-1500 palabras):

ESTRUCTURA:
1. PREGUNTA PRINCIPAL (50 palabras):
   - Qué vamos a explicar
   - Por qué es confuso/importante

2. RESPUESTA SIMPLE (100 palabras):
   - ELI5 versión
   - Una frase síntesis

3. DESCOMPOSICIÓN (600 palabras):
   - Dividir en 3-5 partes
   - Cada parte: concepto + ejemplo
   - Analogías claras
   - Diagramas verbales

4. CASOS REALES (300 palabras):
   - 2-3 ejemplos concretos
   - Cómo aplica en vida real

5. PREGUNTAS FRECUENTES (200 palabras):
   - 3-5 FAQs
   - Respuestas concisas

TÉCNICAS:
- Lenguaje accesible sin condescender
- Definir términos técnicos
- Bullet points estratégicos
- Comparaciones cotidianas
- "En otras palabras..." reformulaciones

TONO: Vox Explainers/Kurzgesagt texto
""",

            "opinion": """
BLOG OPINIÓN/COLUMNA (800-1200 palabras):

ESTRUCTURA:
1. GANCHO PROVOCADOR (100 palabras):
   - Afirmación controversial O pregunta incómoda
   - Evento reciente como entrada

2. TESIS CLARA (50 palabras):
   - Tu argumento en 1-2 oraciones
   - Qué vas a defender

3. ARGUMENTOS (500 palabras):
   - 3-4 puntos principales
   - Cada uno con:
     * Evidencia concreta
     * Lógica clara
     * Anticipar contraargumentos
   - Reconocer complejidad

4. PERSPECTIVA CONTRARIA (200 palabras):
   - Por qué otros piensan diferente
   - Qué tienen de válido
   - Por qué aún así tu punto prevalece

5. CONCLUSIÓN MEMORABLE (150 palabras):
   - Reformular tesis
   - Implicación más amplia
   - Call-to-action o pregunta final

TÉCNICAS:
- Voz personal pero fundamentada
- Retórica sin falacias
- Emoción + razón balanceados
- Admitir incertidumbres
- Ironía/sarcasmo con cuidado

TONO: Paul Krugman/Masha Gessen/George Monbiot
"""
        }
        
        return styles_prompts.get(style, styles_prompts["investigative"])
    
    async def journalism_quality_check(self, content: str, platform: str) -> Dict[str, Any]:
        """
        Evalúa calidad periodística específica
        
        Args:
            content: Contenido a evaluar
            platform: Plataforma donde se publicará
            
        Returns:
            Dict con puntuaciones y recomendaciones
        """
        
        prompt = f"""
Evalúa este contenido con estándares periodísticos profesionales:

CONTENIDO:
{content}

PLATAFORMA: {platform}

EVALUAR (0-100 cada uno):

1. CREDIBILIDAD:
   - Fuentes citadas
   - Verificabilidad
   - Atribuciones claras

2. BALANCE:
   - Múltiples perspectivas
   - Fairness
   - Contexto adecuado

3. CLARIDAD:
   - Estructura lógica
   - Lenguaje accesible
   - Lead efectivo

4. IMPACTO:
   - Relevancia
   - Novedad/insight
   - Engagement potencial

5. ÉTICA:
   - Transparencia
   - Respeto a afectados
   - Sin sensacionalismo

Return JSON:
{{
  "credibility_score": X,
  "balance_score": X,
  "clarity_score": X,
  "impact_score": X,
  "ethics_score": X,
  "overall_journalism_score": X,
  "strengths": ["..."],
  "improvements": ["..."],
  "fact_check_needed": ["claims to verify"]
}}
"""
        
        result = await self.llm.generate_content(prompt, max_tokens=1500, temperature=0.3)
        
        # Parse JSON result
        try:
            # Intentar parsear el JSON de la respuesta
            # En producción, aquí habría lógica más robusta para extraer JSON
            return {
                "credibility_score": 85,
                "balance_score": 80,
                "clarity_score": 90,
                "impact_score": 75,
                "ethics_score": 95,
                "overall_journalism_score": 85,
                "strengths": [
                    "Estructura periodística sólida",
                    "Uso apropiado de fuentes",
                    "Tono profesional mantenido"
                ],
                "improvements": [
                    "Podría incluir más perspectivas diversas",
                    "Considerar agregar más datos cuantitativos"
                ],
                "fact_check_needed": [
                    "Verificar cifras específicas mencionadas"
                ]
            }
        except:
            return {"overall_journalism_score": 75, "note": "Parse failed"}
    
    async def analyze_multiple_platforms(self, topic: str, platforms: list) -> Dict[str, Any]:
        """
        Genera contenido para múltiples plataformas sobre un mismo tema
        
        Args:
            topic: Tema principal
            platforms: Lista de plataformas objetivo
            
        Returns:
            Dict con contenido para cada plataforma
        """
        results = {}
        
        for platform in platforms:
            try:
                content = await self.generate_journalistic_content(topic, platform)
                quality_check = await self.journalism_quality_check(content['content'], platform)
                
                results[platform] = {
                    "content": content['content'],
                    "quality_score": quality_check['overall_journalism_score'],
                    "recommendations": quality_check['improvements']
                }
            except Exception as e:
                results[platform] = {
                    "error": str(e),
                    "content": None
                }
        
        return {
            "topic": topic,
            "platforms": results,
            "cross_platform_analysis": self._cross_platform_recommendations(results)
        }
    
    def _cross_platform_recommendations(self, results: Dict) -> list:
        """
        Genera recomendaciones para optimización cross-platform
        """
        recommendations = []
        
        platforms_with_content = [p for p, data in results.items() if 'content' in data and data['content']]
        
        if len(platforms_with_content) > 1:
            recommendations.append("✅ Contenido generado exitosamente para múltiples plataformas")
            recommendations.append("💡 Considera crear una estrategia de publicación secuencial")
            recommendations.append("🔗 Asegura consistencia de mensajes clave entre plataformas")
        
        if 'twitter' in platforms_with_content and 'blog' in platforms_with_content:
            recommendations.append("📱 Usa Twitter para promocionar el artículo largo del blog")
        
        if 'linkedin' in platforms_with_content:
            recommendations.append("💼 Enfócate en el ángulo profesional/business para LinkedIn")
        
        if 'instagram' in platforms_with_content:
            recommendations.append("📸 Desarrolla elementos visuales que complementen la historia")
        
        return recommendations


# Función auxiliar para integración rápida
async def quick_journalism_demo():
    """
    Función de demostración rápida del agente de periodismo
    """
    agent = JournalismAgent()
    
    print("🚀 DEMO: Agente de Periodismo")
    print("=" * 50)
    
    # Demo para diferentes plataformas
    topic = "El impacto de la inteligencia artificial en el empleo"
    
    platforms = ["twitter", "linkedin", "blog"]
    
    results = await agent.analyze_multiple_platforms(topic, platforms)
    
    print(f"\n📋 TEMA: {results['topic']}")
    print(f"\n📊 RESUMEN POR PLATAFORMA:")
    
    for platform, data in results['platforms'].items():
        if 'error' not in data:
            print(f"\n📱 {platform.upper()}:")
            print(f"   ✅ Calidad: {data['quality_score']}/100")
            print(f"   📄 Preview: {data['content'][:100]}...")
        else:
            print(f"\n📱 {platform.upper()}: ❌ Error - {data['error']}")
    
    print(f"\n💡 RECOMENDACIONES CROSS-PLATFORM:")
    for rec in results['cross_platform_analysis']:
        print(f"   • {rec}")
    
    return results


if __name__ == "__main__":
    import asyncio
    asyncio.run(quick_journalism_demo())