from typing import AsyncGenerator
from libs.vllm.vllm.engine.arg_utils import AsyncEngineArgs
from libs.vllm.vllm.engine.async_llm_engine import AsyncLLMEngine
from libs.vllm.vllm import SamplingParams
from src.model import Model, GeneratorArgs

class VLLM(Model):
    def __init__(self, dir: str, weights: str):
        args = AsyncEngineArgs(weights, download_dir=dir)
        self._engine = AsyncLLMEngine.from_engine_args(args)

    async def generate(self, prompt: str, id: str, args: GeneratorArgs = GeneratorArgs()) -> AsyncGenerator[str, None]:
        params = SamplingParams(temperature=args.temperature, top_p=args.top_p, top_k=args.top_k, max_tokens=args.max_tokens)
        generator = self._engine.generate(prompt, params, id)
        prev = ""
        async for output in generator:
            curr = output.outputs[0].text
            delta = curr[len(prev):]
            prev = curr
            yield delta

    async def abort(self, id: str):
        await self._engine.abort(id)