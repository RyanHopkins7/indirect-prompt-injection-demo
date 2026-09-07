from transformers import AutoModelForCausalLM, AutoTokenizer
from imap_fetch import imap_fetch
from smtp_send import send_email
import json
import logging

logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

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
            "description": "Read the user's emails from their inbox.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "SEND_EMAIL",
            "description": "Send an email.",
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
    "content": "You are Qwen, a helpful email assistant."
}

def model_process_messages(messages):
    print("Messages:", messages)

    text = tokenizer.apply_chat_template(
        messages,
        tools=tools,
        tokenize=False,
        add_generation_prompt=True
    )

    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512,
        do_sample=False
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    if response[:11] == "<tool_call>":
        print(response)

        lines = response.split("\n")
        command = json.loads(lines[1])
        arguments = command["arguments"]
        command_output = ""

        if command["name"] == "READ_EMAILS":
            command_output = imap_fetch()
        elif command["name"] == "SEND_EMAIL":
            command_output = send_email(arguments["sender"], arguments["recipient"], arguments["subject"], arguments["body"])

        return model_process_messages(messages + [{"role": "tool", "content": command_output}])

    return response

while True:
    prompt = input("How can I help you manage your emails today? ")

    response = model_process_messages([system_message, {"role": "user", "content": prompt}])

    print("Qwen: " + response)
