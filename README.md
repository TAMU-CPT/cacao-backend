# CACAO Lite

MediaWiki + php API is a *lot* of cruft for a relatively simple DB model. CACAO
could be reduced significantly to a dead simple API and webapp. This repo will
contain various iterations of that.


## DB Model

- Users
    - name
    - email
- Annotations
    - uuid
    - basically [GAF2.0](http://geneontology.org/page/go-annotation-file-format-20)
    - FK: Users
- Challenge
    - uuid
    - FK: Users
    - FK: Annotations
    - entry type (private, challenge, public)
    - datetime
    - challenge reason
    - points/assement:
        - flagged
            - protein, publication, qualifier, go term, evidence, with/from, notes, unique/original
        - requires changes:
            - go term
        - unacceptable (flags)
        - corrected through challenges
