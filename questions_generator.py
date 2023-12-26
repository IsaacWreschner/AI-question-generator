import openai

openai.api_key = "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"



def generate_questions(text, num_questions=5):

    print(text)
    prompt = f"Generate in GIFT at least 10 questions (Pay attention the questions has to be multichoiced (it may contains choices like 'all true' or 'all false' child level)  based on the following text:\n\n{text}\n\n"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens= 3000,
        stop=None,
        temperature=0.7,
    )

    prompt = f"This following questions are based on this text"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens= 3000,
        stop=None,
        temperature=0.7,
    )

    print(response.choices[0].text)
   
    return response.choices[0].text

