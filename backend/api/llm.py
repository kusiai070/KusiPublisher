import os
from typing import Dict, Any, List
import httpx
import json
import asyncio

from fastapi import HTTPException
class LLMManager:
    def __init__(self):
        self.providers = {
            "gemini": {
                "api_key": os.getenv("GEMINI_API_KEY"),
                "base_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
                "headers": {"Content-Type": "application/json"}
            },
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "base_url": "https://api.openai.com/v1/chat/completions",
                "headers": {"Content-Type": "application/json", "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"}
            },
            "anthropic": {
                "api_key": os.getenv("ANTHROPIC_API_KEY"),
                "base_url": "https://api.anthropic.com/v1/messages",
                "headers": {"Content-Type": "application/json", "x-api-key": os.getenv("ANTHROPIC_API_KEY")}
            }
        }
        
        self.active_provider = os.getenv("ACTIVE_LLM_PROVIDER", "gemini")
        self.cache = {}
    
    async def generate_content(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate content using the active LLM provider with retry logic"""
        
        # Check cache first
        cache_key = f"{self.active_provider}:{prompt[:100]}:{max_tokens}:{temperature}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        provider = self.providers.get(self.active_provider)
        if not provider or not provider["api_key"]:
            raise ValueError(f"Provider {self.active_provider} not configured properly")

        # Lógica de reintentos con espera exponencial
        max_retries = 5
        base_delay = 3  # Empezar con 3 segundos
        for attempt in range(max_retries):
            try:
                # Configurar un timeout más largo (60 segundos)
                timeout = httpx.Timeout(60.0, connect=5.0)
                async with httpx.AsyncClient(timeout=timeout) as client:
                    if self.active_provider == "gemini":
                        payload = { "contents": [{"parts": [{"text": prompt}]}], "generationConfig": { "temperature": temperature, "maxOutputTokens": max_tokens } }
                        
                        print(f"\n--- DEBUG (Attempt {attempt + 1}): Calling Gemini API ---")
                        
                        response = await client.post(f"{provider['base_url']}?key={provider['api_key']}", headers=provider["headers"],
json=payload)
                        result = response.json()
                        
                        print(f"--- DEBUG (Attempt {attempt + 1}): Received response. Status: {response.status_code} ---")

                        if response.status_code >= 500: # Reintentar en errores 5xx
                            raise HTTPException(status_code=response.status_code, detail=result.get("error", {}).get("message", "Gemini server error"))

                        if "candidates" not in result:
                            error_details = result.get("error", {})
                            error_message = error_details.get("message", "Unknown error from Gemini API")
                            # No reintentar en errores de cliente como 'bad request', solo en errores de servidor.
                            raise HTTPException(status_code=400, detail=f"Gemini API Error: {error_message}")

                        content = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    
                    elif self.active_provider == "openai":
                        payload = { "model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": temperature }
                        response = await client.post(provider["base_url"], headers=provider["headers"], json=payload)
                        response.raise_for_status() # Lanza error en respuestas 4xx o 5xx
                        result = response.json()
                        content = result["choices"][0]["message"]["content"]
                
                # Éxito, guardar en caché y devolver
                self.cache[cache_key] = content
                return content
            
            except (httpx.ReadTimeout, httpx.ConnectError, HTTPException) as e:
                is_retryable = False
                if isinstance(e, HTTPException):
                    if e.status_code in [500, 503, 504]: # Errores de servidor
                        is_retryable = True
                else: # Timeout o error de conexión
                    is_retryable = True

                if is_retryable and attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    error_msg = e.detail if isinstance(e, HTTPException) else str(e)
                    print(f"--- WARNING: API call failed (attempt {attempt + 1}/{max_retries}). Retrying in {delay}s... Error: {error_msg} ---")
                    await asyncio.sleep(delay)
                else:
                    print(f"--- ERROR: API call failed after {max_retries} attempts. ---")
                    if isinstance(e, HTTPException): # Si es nuestro error, lo relanzamos
                        raise e
                    else: # Si es de httpx, lo envolvemos
                        raise HTTPException(status_code=504, detail=f"Gateway Timeout: {str(e)}")
        
        async def analyze_text(self, text: str, analysis_type: str) -> Dict[str, Any]:
            """Analyze text for various attributes"""
            
            prompts = {
                "voice_analysis": f"""
                    Analyze the following text for voice and style characteristics:
                    Text: {text}
                    
                    Provide a detailed analysis including:
                    - Tone (formal, casual, friendly, professional, etc.)
                    - Writing style (conversational, academic, persuasive, etc.)
                    - Key personality traits
                    - Common phrases or patterns
                    - Emotional resonance
                    
                    Return as JSON format.
                """,
                "quality_check": f"""
                    Analyze the quality of this content:
                    Text: {text}
                    
                    Check for:
                    - Grammar and spelling errors
                    - Clarity and readability
                    - Engagement potential
                    - Platform appropriateness
                    - SEO optimization
                    
                    Provide a quality score (0-100) and specific suggestions for improvement.
                    Return as JSON format.
                """,
                "seo_analysis": f"""
                    Analyze this content for SEO optimization:
                    Text: {text}
                    
                    Identify:
                    - Primary keywords
                    - Secondary keywords
                    - Suggested hashtags
                    - Readability score
                    - Emotional triggers
                    - Call-to-action opportunities
                    
                    Return as JSON format.
                """
            }
            
            prompt = prompts.get(analysis_type)
            if not prompt:
                raise ValueError(f"Unknown analysis type: {analysis_type}")
            
            result = await self.generate_content(prompt, max_tokens=2000, temperature=0.3)
            
            try:
                # Try to parse JSON from the response
                import json
                # Extract JSON if it's embedded in text
                json_start = result.find('{')
                json_end = result.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = result[json_start:json_end]
                    return json.loads(json_str)
                return {"analysis": result}
            except:
                return {"analysis": result}
        
        def switch_provider(self, provider: str):
            """Switch to a different LLM provider"""
            if provider in self.providers:
                self.active_provider = provider
            else:
                raise ValueError(f"Unknown provider: {provider}")
        
        def get_available_providers(self) -> List[str]:
            """Get list of available providers"""
            return [name for name, config in self.providers.items() if config["api_key"]]