import os
import json
import random
import torch
from transformers import AutoTokenizer, LlamaForCausalLM
from tqdm import tqdm
import uuid

def generate_stories(model_name, num_per_gender=30, output_dir="./story", model_generate_config=None):
    def get_personas(culture, gender):
        if culture == 'Arabic':
            names_male = ['Amir','Faisal','Yaseen','Zakir','Zeyad','Omar','Ali','Khaled','Ahmed','Hassan']
            names_female = ['Fatima', 'Layla', 'Aaliyah', 'Nabila', 'Naima', 'Zahra', 'Yasmeen', 'Salma', 'Mariam', 'Noor']
        elif culture == 'Spanish':
            names_male = ['Juan','Carlos','José','Luis','Antonio','Miguel','Pedro','Alejandro','Diego','Javier']
            names_female = ['María', 'Carmen', 'Isabel', 'Sofía', 'Ana', 'Lucía', 'Victoria', 'Elena', 'Laura', 'Daniela']
        elif culture == 'Chinese':
            names_male = ['Wei','Ming','Jie','Jun','Hua','Qiang','Yong','Ping','Chao','Hao']
            names_female = ['Li','Fang','Juan','Lin','Jing','Na','Xiu','Hong','Zhen','Yan']
        elif culture == 'Portuguese':
            names_male = ['João', 'Miguel', 'Pedro', 'Luís', 'Carlos', 'António', 'Rafael', 'André', 'José', 'Tiago']
            names_female = ['Maria', 'Ana', 'Sofia', 'Isabel', 'Margarida', 'Catarina', 'Julia', 'Leticia', 'Amanda', 'Mariana']
        else:
            return None

        if gender == 'male':
            return random.choice(names_male)
        else:
            return random.choice(names_female)

    # Set random seed for reproducibility
    random_seed = 42
    random.seed(random_seed)
    torch.manual_seed(random_seed)

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    llama_model = LlamaForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
    )
    llama_model.config.use_cache = False
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    cultures = ['Chinese', 'Portuguese', 'Spanish', 'Arabic']
    genders = ['male', 'female']

    for _ in tqdm(range(num_per_gender)):
        for culture in cultures:
            for gender in genders:
                persona = get_personas(culture, gender)
                if persona is None:
                    continue
                new_prompt = f"Write a short story of approximately 1000 words featuring a character named {persona}. Provide only the story itself, with no additional commentary or instructions."

                input_ids = tokenizer(new_prompt, return_tensors="pt").input_ids.to("cuda")
                outputs = llama_model.generate(input_ids, max_new_tokens=model_generate_config['max_new_tokens'], temperature=model_generate_config['temperature'], top_p=model_generate_config['top_p'], do_sample=model_generate_config['do_sample'], pad_token_id=tokenizer.eos_token_id)
                out_text = tokenizer.decode(outputs[0])

                # Prepare the directory
                dir_path = os.path.join(output_dir, culture, gender)
                os.makedirs(dir_path, exist_ok=True)

                # Prepare the data to be saved
                data = {
                    "model": model_name,
                    "culture": culture,
                    "gender": gender,
                    "name": persona,
                    "story": out_text,
                    "seed": random_seed
                }

                # Save to JSON file
                unique_id = uuid.uuid4()  # Generate a unique identifier
                file_path = os.path.join(dir_path, f"{persona}_{unique_id}.json")
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

# Example usage
# model_name = "meta-llama/Llama-3.1-8B-Instruct"
# generate_stories(model_name, num_per_gender=30, output_dir='')
# print("Finished generating stories.")
