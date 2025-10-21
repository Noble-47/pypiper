from pypiper.annotations import Depends, PipelineState
from pypiper.datamodels import FileSource
from pypiper import Pipeline

pipeline = Pipeline(name = "Document Processor", source = FileSource("path_to_document.txt"))

@pipeline.register_task()
def category_classification(text:Annotated[str, Depends("source")]):
    classification_model = ClassificationModel()
    output = [(category, score) for category, score in classification_model.predict(text)]
    return output

@pipeline.register_task()
def keyword_extraction(text:Annotated[str, Depends("source")], category_classes:Annotated[list[tuple], Depends("category_classification")]):
    keyword_extractor = KeywordExtractionModel()
    for category, score in category_classes:
        keywords[category] = KeywordExtractionModel(category, text)
    return keywords

@pipeline.register_task()
def report_generator(category_classes : Annotated[list, Depends("category_classification")], keywords : Annotated[Depends("keyword_extraction")]):
    detected_categories = [ {'category' : category, 'score' : score} for category, score in category_classes.items()]
    summary = {
        "detected_categories" : detected_categories,
        "keywords_extracted" : keyword_extracted,
    }
    return summary


pipeline.run()

