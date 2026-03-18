# The Moralization Corpus
This repository provides the full source code and supplementary materials for the paper: ["The Moralization Corpus: Frame-Based Annotation and Analysis of
Moralizing Speech Acts across Diverse Text Genres"](https://arxiv.org/abs/2512.15248) (Becker et al., LREC 2026).

Please feel free to contact us via e-mail (maria.becker@gs.uni-heidelberg.de; sommer@cl.uni-heidelberg.de) with any questions, comments, or feedback.

## Abstract
Moralizations – arguments that invoke moral values to justify demands or positions – are a yet underexplored form of persuasive communication. We present the Moralization Corpus, a novel multi-genre dataset designed to analyze how moral values are strategically used in argumentative discourse. Moralizations are pragmatically complex and often implicit, posing significant challenges for both human annotators and NLP systems. We develop a frame-based annotation scheme that captures the constitutive elements of moralizations – moral values, demands, and discourse protagonists – and apply it to a diverse set of German texts, including political debates, news articles, and online discussions. The corpus enables fine-grained analysis of moralizing language across communicative formats and domains. We further evaluate several large language models (LLMs) under varied prompting conditions for the task of moralization detection and moralization component extraction and compare it to human annotations in order to investigate the challenges of automatic and manual analysis of moralizations. Results show that detailed prompt instructions has a greater effect than few-shot or explanation-based prompting, and that moralization remains a highly subjective and context-sensitive task. We release all data, annotation guidelines, and code to foster future interdisciplinary research on moral discourse and moral reasoning in NLP.

## Data

- Annotated Dataset: [http://corpora.ids-mannheim.de/repo/moralization-corpus/](http://corpora.ids-mannheim.de/repo/moralization-corpus/)
- Predictions from LLMs: [data/predictions.json](data/predictions.json)
- IAA Study [data/iaa-study_test-150.tsv](data/iaa-study_test-150.tsv)
- Dictionary of Moral-Indicating Words: [DiMi](https://github.com/maria-becker/Moralization/tree/main/DiMi%20--%20Dictionary%20of%20Moral-Indicating%20Words)



## Citation
```
@misc{becker2025moralizationcorpusframebasedannotation,
      title={The Moralization Corpus: Frame-Based Annotation and Analysis of Moralizing Speech Acts across Diverse Text Genres}, 
      author={Maria Becker and Mirko Sommer and Lars Tapken and Yi Wan Teh and Bruno Brocai},
      year={2026},
      eprint={2512.15248},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2512.15248}, 
}
```
