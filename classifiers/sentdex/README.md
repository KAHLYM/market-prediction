# sentdex

Credit to [@Sentdex](https://twitter.com/sentdex) for providing the [NLTK with Python 3 for Natural Language Processing](https://www.youtube.com/playlist?list=PLQVvvaa0QuDf2JswnfiGkliBInZnIC4HL) for which the containing files are based upon.

## Example

    s = __import__('sentiment_mod')
    
    print(s.sentiment("This movie was awesome! The acting was great, plot was wonderful, and there were pythons...so yea!"))
    print(s.sentiment("This movie was utter junk. There were absolutely 0 pythons. I don't see what the point was at all. Horrible movie, 0/10"))
    print(s.sentiment("This movie was awesome but also utter junk"))

    # Output
    # ('pos', 1.0)
    # ('neg', 1.0)
    # ('neg', 0.8)
