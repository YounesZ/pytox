import json
import aiofiles


async def async_load_json(filepath):

    async with aiofiles.open(filepath, 'r') as file:
        content = await file.read()

    return json.loads(content)





if __name__ == '__main__':

    import asyncio
    from apps.localvars import PATH_TO_SCRAPY_OUTPUT

    async def main():
        output = await async_load_json(filepath=PATH_TO_SCRAPY_OUTPUT)
        return output

    output = asyncio.run(main())
    print(output)