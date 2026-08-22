from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen2.5-1.5B-Instruct"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

tools = [
    {
        "type": "function",
        "function": {
            "name": "READ_EMAILS",
            "description": "Read the user's emails from their inbox",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "SEND_EMAIL",
            "description": "Send an email",
            "parameters": {
                "type": "object",
                "properties": {
                    "sender": {"type": "string"},
                    "recipient": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"}
                },
                "required": ["sender", "recipient", "subject", "body"]
            }
        }
    }
]
system_message = {
    "role": "system", 
    "content": "You are Qwen, a helpful email assistant. Your job is to help the user manage their emails and perform any email-related tasks."
}

while True:
    prompt = input("How can I help you manage your emails today? ")

    text = tokenizer.apply_chat_template(
        [
            system_message, 
            {
                "role": "user",
                "content": prompt
            }
        ],
        tools=tools,
        tokenize=False,
        add_generation_prompt=True
    )

    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=1024,
        do_sample=False
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(response)
