import requests
from app.config import Config
import google.generativeai as genai

class LogService:
    def generate_log(self, code, language, prefix, suffix, api_provider):
        if api_provider == 'openai':
            return self.call_openai(code, language, prefix, suffix)
        elif api_provider == 'gemini':
            return self.call_gemini(code, language, prefix, suffix)
        else:
            return None
    def call_openai(self, code, language, prefix, suffix):
        try:
            response = requests.post(
                'https://api.openai.com/v1/completions',
                headers={
                    'Authorization': f'Bearer {Config.OPENAI_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'text-davinci-002',
                    'prompt': self.generate_prompt(code, language, prefix, suffix),
                    'max_tokens': 50
                }
            )
            response_json = response.json()
            log_message = response_json['choices'][0]['text'].strip()
            return log_message
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return None
    def call_gemini(self, code, language, prefix, suffix):
        # Placeholder for Gemini API call implementation
        try : 
            genai.configure(api_key=Config.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.0-pro')
            response = model.generate_content(self.generate_prompt(code, language, prefix, suffix))
            print(response.text)
            # log_message = response_json['choices'][0]['text'].strip()
            return response.text
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            return None
        # try:
        #     response = requests.post(
        #         'https://api.gemini.com/v1/completions',  # Update with actual Gemini API endpoint
        #         headers={
        #             'Authorization': f'Bearer {Config.GEMINI_API_KEY}',
        #             'Content-Type': 'application/json'
        #         },
        #         json={
        #             'model': 'text-davinci-002',  # Update with actual Gemini model
        #             'prompt': self.generate_prompt(code, language, prefix, suffix),
        #             'max_tokens': 50
        #         }
        #     )
        #     response_json = response.json()
        #     print(response_json)
        #     log_message = response_json['choices'][0]['text'].strip()
        #     return log_message
        # except Exception as e:
        #     print(f"Error calling Gemini: {e}")
        #     return None
    # def generate_prompt(self, code, language, prefix, suffix):
    #     code = """const getDevice = (deviceId: number) => {
    #         return api
    #             .get(`${nameSpace}/${deviceId}`)
    #             .then((res) => new AgentDevice().deserialize(res))
    #             .catch((e) => reject(e));
    #         };"""
    #     return f"Generate an insightful and efficient debug log for the following {language} code:\n\n{code}\n\nThe log should provide detailed information to help a developer understand and debug the code efficiently. Use the prefix \"{prefix}\" and the suffix \"{suffix}\" for the log message."
    def generate_prompt(self, code, language, prefix, suffix):
        # code = """
        # const getDevice = (deviceId: number) => {
        #     return api
        #         .get(`${nameSpace}/${deviceId}`)
        #         .then((res) => new AgentDevice().deserialize(res))
        #         .catch((e) => reject(e));
        #     };"""
        return (
            f"Generate debug log statements to print in logs for the following {language} code. "
            f"Each log statement should capture key values and states necessary for debugging. "
            f"Ensure the log statements are inserted at critical points in the code such as variable assignments, "
            f"function entries and exits, and key decision points. "
            f"Do not include any explanations or comments. "
            f"\n\n{code}"
            f"\n\n note that the provided code should not be changed including the intendation only print statements lines should be added according to language provided"
        )
