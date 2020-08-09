"""Search for a specific part of speech in the text.

POS search algorithm in the text.
- Prepare raw text.
- Use the NLP model.
- Matching
- Return results.
"""

import nlp.processing.text_processor as tp


def pos_tag_search(nlp, text, pos_tag):
    """Search for a specific part of speech.

    Parameters
    ----------
    nlp : nlp
        Prepared nlp model

    text : str
        Text for analysis.

    pos_tag: str
        The desired part of speech.

    Returns
    -------
    result: list
       List of tokens and their indices.
    """

    text = tp.lexical_processor(text)

    # Create flexible batches (split at the end of the sentence)
    batch_indices = tp.flexible_batch_indices(text, 1000)
    text_split = [text[batch_indices[i - 1]:batch_indices[i]] for i in range(1, len(batch_indices))]

    # Apply the model to batches
    docs = list(nlp.pipe(text_split))

    # Lists needed to return a result
    tokens = []
    tokens_indices = []
    tokens_pos = []

    # Specific or all POS are needed
    include_all_pos = pos_tag == 'ALL'
    for cur_batch, doc in enumerate(docs):
        batch_idx = batch_indices[cur_batch]
        for token in doc:
            # Check compliance with the requirement and not equality with the punctuation mark
            if (token.pos_ == pos_tag or include_all_pos) and token.pos_ != 'PUNCT':
                tokens.append(token.text)
                tokens_indices.append([batch_idx + token.idx,
                                       batch_idx + token.idx + len(token)])
                if include_all_pos:
                    tokens_pos.append(token.pos_)

    result = [tokens, tokens_indices]

    # Append POS Tags only if all is needed
    if include_all_pos:
        result.append(tokens_pos)

    return result
