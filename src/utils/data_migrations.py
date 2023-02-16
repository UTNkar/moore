from django.core.serializers.json import DjangoJSONEncoder
from wagtail.core.blocks.stream_block import StreamValue
from json import dumps

"""
Recursively apply a filter-map operation on a block by traversing
it and its children, and calling the mapper_func on each block whose
'type' value matches block_type.

:param block: The block to apply the filter-map operation on
:param block_type: The type of blocks to apply the mapper_func on
:param mapper_func: Function that takes a block and returns a new
 transformed block
:return: Returns a new block hierarchy with the matched blocks
 transformed
"""


def block_filter_map(block, block_type, mapper_func):
    if isinstance(block, list):
        for i in range(len(block)):
            block[i] = block_filter_map(block[i], block_type, mapper_func)
    if isinstance(block, dict):
        if 'type' in block and block['type'] == block_type:
            block = mapper_func(block)
        else:
            for k, v in block.items():
                block[k] = block_filter_map(v, block_type, mapper_func)

    return block


"""
Recursively apply a filter operation on a block by traversing it
and its children, and calling the predicate_func on each block. Only
the blocks that make predicate_func return true are returned back, the
others have their values cleared. Important: Does not deep copy by
itself. Make sure to perform a deep copy beforehand!

:param block: The block to apply the filter-map operation on
:param predicate_func: Function that decides wether or not the block
is filtered
:return: Returns a block hierarchy only containing the passing blocks.
"""


def block_filter(block, predicate_func):
    if isinstance(block, list):
        for i in range(len(block)):
            block[i] = block_filter(block[i], predicate_func)
    elif isinstance(block, dict):
        if 'type' in block:
            # This is a proper block
            if predicate_func(block):
                for k, v in block.items():
                    block[k] = block_filter(v, predicate_func)
            else:
                return {'type': block['type'], 'value': {}}

    # int or string or something, just return untouched
    return block


"""
Recursively apply a filter-map operation on a stream field,
replacing every block or sub-block with the same type as block_type
with the blocks produced by applying the mapper_func.

:param stream_field: The StreamValue to apply the filter-map operation
 on
:param block_type: The type of blocks to apply the mapper_func on
:param mapper_func: Function that takes a block and returns a new
 transformed block

:returns: A new StreamValue with all the blocks and sub-blocks whose
 type matches block_type transformed by mapper_func
"""


def stream_field_filter_map(stream_field, block_type, mapper_func):
    new_stream_data = []
    for block in stream_field.raw_data:
        new_stream_data.append(
            block_filter_map(block, block_type, mapper_func)
        )
    raw_text = dumps(new_stream_data, cls=DjangoJSONEncoder)
    stream_block = stream_field.stream_block
    return StreamValue(stream_block, [], is_lazy=True, raw_text=raw_text)
