import spacy
from spacy.matcher import Matcher

class Word_Extraction:
    def __init__(self, word_types=None):
        """
        初始化 Word_Extraction 类。
        根据传入的 word_types 初始化 SpaCy 模型和模式匹配器。

        参数:
            word_types (list): 包含词性类别的列表，例如 ['noun', 'adj', 'verb']。
        """
        self.nlp = spacy.load("en_core_web_sm")  # 加载 SpaCy 的小型英文模型
        self.matcher = Matcher(self.nlp.vocab)  # 创建模式匹配器
        patterns = []

        for word_type in word_types:
            if word_type == 'noun':
                patterns.append([{'POS': 'NOUN'}])  # 匹配名词
            elif word_type == 'adj':
                patterns.append([{'POS': 'ADJ'}])  # 匹配形容词
            elif word_type == 'verb':
                patterns.append([{'POS': 'VERB'}])  # 匹配动词

        self.matcher.add("word_type_matcher", patterns)  # 添加匹配模式

    def extract_word(self, text):
        """
        从输入文本中提取指定类型的单词。

        参数:
            text (str): 输入文本。

        返回:
            list: 匹配到的单词列表。
        """
        doc = self.nlp(text)  # 分词并标注词性
        matches = self.matcher(doc)  # 进行模式匹配
        extracted_words = [doc[start:end].text for _, start, end in matches]  # 提取匹配到的单词
        return extracted_words


# 测试代码
if __name__ == "__main__":
    # 初始化提取器
    noun_extractor = Word_Extraction(['noun'])  # 提取名词
    adj_extractor = Word_Extraction(['adj'])  # 提取形容词

    # 输入文本
    sample_text = "This is a fantastic opportunity for students to learn."

    # 提取名词
    nouns = noun_extractor.extract_word(sample_text)
    print("Extracted nouns:", nouns)

    # 提取形容词
    adjectives = adj_extractor.extract_word(sample_text)
    print("Extracted adjectives:", adjectives)
