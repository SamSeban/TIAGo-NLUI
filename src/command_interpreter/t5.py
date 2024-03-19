from transformers import T5ForConditionalGeneration, T5Tokenizer

class T5CommandInterpreter:
    def __init__(self, model_dir="./models/t5_finetuned"):
        """
        Initializes the command interpreter with the fine-tuned T5 model.
        """
        self.tokenizer = T5Tokenizer.from_pretrained(model_dir)
        self.model = T5ForConditionalGeneration.from_pretrained(model_dir)

    def interpret_command(self, command_text):
        """
        Interprets a natural language command into a structured form or specific action using T5.
        """
        input_ids = self.tokenizer.encode(command_text, return_tensors="pt")
        output_ids = self.model.generate(input_ids, max_length=50)
        interpreted_command = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return interpreted_command
