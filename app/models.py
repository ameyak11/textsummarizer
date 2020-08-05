class DemoSummarizerArticle():
    def get_dict(self):
        article = {}
        article['article_title'] = self.title
        article['article_body'] = self.article_body
        article['summary_indices'] = self.summary_indices
        return article




