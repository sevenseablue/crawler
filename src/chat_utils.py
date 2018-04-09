# codint: utf8


from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

deepThought = ChatBot("deepThought")
deepThought.set_trainer(ChatterBotCorpusTrainer)
# 使用中文语料库训练它
deepThought.train("chatterbot.corpus.chinese")  # 语料库

