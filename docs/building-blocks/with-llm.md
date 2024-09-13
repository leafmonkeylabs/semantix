# With LLM

## What is `with_llm`?

With LLM is a Python decorator that allows you to automatically augment functions with LLM-powered capabilities. By adding the `@with_llm` decorator to a function, you can create super intelligent functions that doesnt even need a code body.

Here's an example of how you can use the `@with_llm` decorator to enhance a function with LLM-powered capabilities:

```python
from semantix import with_llm
from semantix.llms import OpenAI


@with_llm("Convert the Given Sentence to Arabic", llm=OpenAI())
def translate_to_arabic(sentence: str) -> str:
    ...
```

In this example, the `@with_llm` decorator is used to enhance the `translate_to_arabic` function with the ability to convert a given sentence to Arabic using OpenAI's LLM. The function signature remains the same, but the function now has the added capability of leveraging the power of LLMs to perform the translation.

You can use the resulting function just like any other function, but with the added intelligence provided by the LLM. This allows you to write more expressive, powerful code without having to explicitly call the LLM in your code.

## How `with_llm` Works?

The `@with_llm` decorator works by wrapping the original function with a new function that handles the LLM logic. When the enhanced function is called, the LLM logic is executed behind the scenes, and the result is returned to the caller.

`with_llm` uses the function name, function signature and types, output hint and docstring to generate meaningful inputs for the LLMs. It doesnt send your code or anything else to the LLMs.

Behind the scenes, `with_llm` uses a prompting techniques called `Meaning Typed Prompting` to generate the prompts for the LLMs. This allows the LLMs to understand the context and meaning of the function, relationship between the types and generate more accurate, correctly typed outputs.

When the resulting function is executed with necessary inputs, `with_llm` with apply the inputs to the generated prompt, gets the output from the LLM, convert the output to the expected type, and if ran into any error it will run self correction mechanism to correct the output.

## Why Use `with_llm`?

The `with_llm` decorator provides a simple and powerful way to infuse intelligence into your functions without having to write complex LLM logics or do manually prompting work. By leveraging the power of LLMs behind the scenes, you can create functions that are context-aware, intelligent, and capable of performing complex tasks with ease.