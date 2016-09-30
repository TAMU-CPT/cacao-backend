# CACAO Lite

[![Build Status](https://travis-ci.org/elenimijalis/cacao-lite.svg)](https://travis-ci.org/elenimijalis/cacao-lite)

MediaWiki + php API is a *lot* of cruft for a relatively simple DB model. CACAO
could be reduced significantly to a dead simple API and webapp. This repo will
contain various iterations of that.


## DB Model

- Users
    - (you can use, unmodified, the default django user class)
- Teams
    - team name
    - M2M on users
- Annotations
    - uuid
    - basically [GAF2.0](http://geneontology.org/page/go-annotation-file-format-20)
    - FK: Users
- Challenges
    - uuid
    - FK: Users
    - FK: Annotations
    - entry type (private, challenge, public)
    - datetime
    - challenge reason

- Assessment
    - FK: Annotations (null=True, blank=True)
    - FK: Challenges (null=True, blank=True)
    - flagged (can be flagged for multiple reasons, such as the following)
        - protein, publication, qualifier, go term, evidence, with/from, notes, unique/original

GOA for obtaining existing GAF (https://www.ebi.ac.uk/GOA/downloads)

## JBrowse Integration

```JSON
{
  "label": "my_rest_track",
  "key": "REST Test Track",
  "storeClass": "JBrowse/Store/SeqFeature/REST",
  "baseUrl": "https://server_url/jbrowse/",
  "query": {
    "organism": "Miro"
  },
  "style": {
    "color": "function(feature){ if(feature.data.state == 1){ return 'yellow'; } if(feature.data.state == 2){ return 'green';} return 'red';}"
  },
  "type": "JBrowse/View/Track/CanvasFeatures",
  "trackType": "JBrowse/View/Track/CanvasFeatures"
}
```

## License
This software is licensed under AGPL-3.0.
