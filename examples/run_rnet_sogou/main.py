import sys
sys.path.append('../..')
import logging
import torch
from pytorch_mrc.dataset.squad import SquadReader, SquadEvaluator
from pytorch_mrc.model.rnet_sogou import RNET
from pytorch_mrc.data.batch_generator import BatchGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
bg_folder = '/home/len/yingzq/nlp/mrc_dataset/squad-v1.1/bg_data/'
train_bg_file = bg_folder + "bg_train_50b_300d_uncased.pkl"
eval_bg_file = bg_folder + "bg_eval_50b_300d_uncased.pkl"
dev_file = "/home/len/yingzq/nlp/mrc_dataset/squad-v1.1/dev-v1.1.json"

reader = SquadReader(fine_grained=True)
eval_data = reader.read(dev_file)
evaluator = SquadEvaluator(dev_file)

train_batch_generator = BatchGenerator()
eval_batch_generator = BatchGenerator()
train_batch_generator.load(train_bg_file)
eval_batch_generator.load(eval_bg_file)
vocab = train_batch_generator.get_vocab()

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = RNET(vocab, device, pretrained_word_embedding=vocab.get_word_embedding(), word_embedding_size=300)
model.compile('adam', 0.001)
model.train_and_evaluate(train_batch_generator, eval_batch_generator, evaluator, epochs=200, episodes=2)
