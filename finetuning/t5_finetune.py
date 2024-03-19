from transformers import T5Tokenizer
from transformers import T5ForConditionalGeneration, Trainer, TrainingArguments
from datasets import load_dataset, DatasetDict, Features, Value

from datasets import load_dataset

# Specify the paths to your train and test dataset files
data_files = {
    "train": "./data/train.json", 
    "test": "./data/test.json"
}

# Load the datasets
dataset = load_dataset('json', data_files=data_files)

# Initialize the tokenizer
tokenizer = T5Tokenizer.from_pretrained('t5-small')

# Tokenize the input and output
def tokenize_function(examples):
    input_encodings = tokenizer(examples['input'], padding="max_length", truncation=True, max_length=128)
    output_encodings = tokenizer(examples['output'], padding="max_length", truncation=True, max_length=128)
    return {"input_ids": input_encodings.input_ids, "attention_mask": input_encodings.attention_mask, "labels": output_encodings.input_ids}

tokenized_datasets = dataset.map(tokenize_function, batched=True)

model = T5ForConditionalGeneration.from_pretrained('t5-small')

training_args = TrainingArguments(
    output_dir='./models/t5_finetuned',          # output directory for model and checkpoints
    num_train_epochs=50,              # total number of training epochs
    per_device_train_batch_size=2,   # batch size per device during training
    per_device_eval_batch_size=2,    # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./models/t5_finetuned/logs',            # directory for storing logs
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['test'],
)

trainer.train()
trainer.save_model(training_args.output_dir)
tokenizer.save_pretrained(training_args.output_dir)

# To load the model
model = T5ForConditionalGeneration.from_pretrained("./models/t5_finetuned")
