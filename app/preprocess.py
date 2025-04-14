
import os
os.environ['CUDA_VISIBLE_DEVICES'] = "0"

import spacy
import logging
import nltk
nltk.download('punkt',quiet=True)
nltk.download('punkt_tab', quiet=True)
import click
from nltk.tokenize import sent_tokenize

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO",
)

import json, re
nlp = spacy.load('en_coreference_web_trf')

def extract_content(text):
    
    md_content = [k.strip() for k in text.split('\n')]
    
    # Initialize lists for extracted elements
    titles = []
    content = []
    current_paragraph = []
    
    # Process each line
    for line in md_content:
        line = line.strip()
        
        # Extract titles (lines starting with #)
        if line.startswith('#'):
            titles.append(line.lstrip('#').strip())
            if current_paragraph:
                content.append(' '.join(current_paragraph))
                current_paragraph = []
        
        # Extract bullet points (lines starting with * or - or numbered lists)
        elif re.match(r'^[*\-]|^\d+\.', line):
            content.append(line.lstrip('*-').strip())
            if current_paragraph:
                content.append(' '.join(current_paragraph))
                current_paragraph = []
        
        # Extract paragraphs (lines that are not empty and not part of titles or bullet points)
        elif line:
            current_paragraph.append(line)
        
        # Store collected paragraph if an empty line is encountered
        else:
            if current_paragraph:
                content.append(' '.join(current_paragraph))
                current_paragraph = []
    
    # Ensure last paragraph is added
    if current_paragraph:
        content.append(' '.join(current_paragraph))
    
    return titles, content

def resolve_references(sent):

    doc = nlp(sent)
    token_mention_mapper = {}
    output_string = ""
    clusters = [
        val for key, val in doc.spans.items() if key.startswith("coref_cluster")
    ]

    for cluster in clusters:
        first_mention = cluster[0]
        for mention_span in list(cluster)[1:]:
            token_mention_mapper[mention_span[0].idx] = first_mention.text + mention_span[0].whitespace_

            for token in mention_span[1:]:
                token_mention_mapper[token.idx] = ""

    for token in doc:
        if token.idx in token_mention_mapper:
            output_string += token_mention_mapper[token.idx]
        else:
            output_string += token.text + token.whitespace_

    return output_string

def preprocess(content, md=True):
    
    if md:
        titles, paragraphs = extract_content(content)
        print("Using md ...")
        
    else:
        text = content.replace('*', '').replace('#', '').replace('-', '').replace('\xa0', ' ')

        paragraphs = text.split('\n\n')
        print("Using old ...")
        
    coref_resolved = [resolve_references(k) for k in paragraphs]

    preprocessed_lines = []
    for p in coref_resolved:
        preprocessed_lines.extend(p.split('\n'))
    sents = []
    for p in preprocessed_lines:
        sents.extend(sent_tokenize(p))

    return sents

@click.command()
@click.option('--policy_doc', default='privacy_hotcrp.md',
              help='High-level requirement specification document',
              show_default=True,
              required=True,
              )
def main(policy_doc):
    print("\n ============================= Starting AGentV =============================\n")
    logging.info(f"Policy document: {policy_doc}")
    sents = preprocess(policy_doc)
    with open('../data/high_level_requirements.json', 'w') as f:
        json.dump(sents, f)
    logging.info("Preprocessing is completed!")


if __name__ == '__main__':
    main()