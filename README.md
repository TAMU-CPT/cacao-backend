# CACAO Backend

This is the backend for CACAO, or Community Annotation of Community Assessment
with Ontologies. The current MediaWiki + php API is very complex for these DB
models, so we reduced CACAO to a simpler API and web app.

## Usage
### Set up a virtual environment and install requirements
```console
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```
### Migrate
```console
$ python manage.py migrate
```
### Load fixtures
We've created some sample data:
```console
$ python manage.py loaddata fixtures/
```
#### Run
```console
$ python manage.py runserver
```

## JBrowse Integration
If you want to view your annotations in JBrowse, add the following to your
trackList.json file and point it at your backend url.

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
