'''
Jayden Zhang, Margie Cao, Danny Huang, Kyle Lee
404NotFound
SoftDev
P04
Time spent: tbd
Target Ship Date: 2025-06-06
'''
import time
from google import genai
from google.genai import types

def getGeminiExplaination(key, prompt):
    try: 
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction="You are a teacher, explaining the answer to a student."),
            contents=prompt
        )
        return response.text
    except Exception as e:
        return None

def getGeminiVideo(key,prompt):
    try: 
        client = genai.Client(api_key=key)
        operation = client.models.generate_videos(
            model="veo-2.0-generate-001",
            prompt=prompt,
            config=types.GenerateVideosConfig(
                system_instruction="Create a khan academy style video that writes out the step by step solution",
                person_generation="dont_allow",  
                aspect_ratio="16:9",  
            ),
        )
        while not operation.done:
            time.sleep(20)
            operation = client.operations.get(operation)

        for n, generated_video in enumerate(operation.response.generated_videos):
            client.files.download(file=generated_video.video)
            generated_video.video.save(f"video{n}.mp4")
        return n
    except Exception as e:
        return None
'''I didn't push to init, put the following code in solutions routing if you want to try to play with it
uploaded_file = request.files.get("file")
        if api_key and prompt:
            explanation = sol.getGeminiExplaination(api_key, prompt)
            video = sol.getGeminiVideo(api_key, prompt)
        if api_key and uploaded_file:
            explanation = sol.getGeminiVideo(api_key, uploaded_file)'''
def getGeminiVideo(key, image):
    try:
        client = genai.Client(api_key=key)
        imageBytes = image.read()
        imagePart = types.Blob(mime_type=image.mimetype, data=imageBytes)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[imagePart, "Explain This problem"]
        )
        return response.text
    except Exception as e:
        return None
