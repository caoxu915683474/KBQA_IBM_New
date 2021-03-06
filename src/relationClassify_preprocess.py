import gzip
import nltk
import string
import codecs
import operator
import numpy
import heapq
from operator import itemgetter
import time
from random import shuffle, sample

# def last_slash_pos(str):
#     return str.rfind('/')
# def last_dot_pos(str):
#     return str.rfind('.')
# def extract_related_triples():
#     #load freebase2M as map
#     head2tripleSet={}
#     read_freebase=open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/freebase-subsets/freebase-FB2M-ungrouped.txt', 'r')
#     count=0
#     for line in read_freebase:
#         parts=line.strip().split()
#         head=parts[0][last_slash_pos(parts[0])+1:]
#         relation=parts[1][last_slash_pos(parts[1])+1:]
#         tail=parts[2][last_slash_pos(parts[2])+1:]
#         tripleSet=head2tripleSet.get(head)
#         if tripleSet is None:
#             tripleSet=set()           
#         tripleSet.add((head, relation, tail))
#         head2tripleSet[head]=tripleSet
# #         print head2tripleList
# #         exit(0)
#         count+=1
#     read_freebase.close()
#     print 'Freebase has totally', count, 'triples'
#     
#     #extend SimpleQuestion by negative triples
#     SQs=['annotated_fb_data_train', 'annotated_fb_data_test', 'annotated_fb_data_valid']
#     max_triples=0
#     min_triples=10000
#     
#     for SQ in SQs:
#         zero_nega=0
#         read_SQ=open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'+SQ+'.txt', 'r')
#         write_SQ=open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'+SQ+'_PNQ.txt', 'w')
#         for line in read_SQ:
#             parts=line.strip().split('\t')
#             Q=parts[3]
#             head=parts[0][last_slash_pos(parts[0])+1:]
#             relation=parts[1][last_slash_pos(parts[1])+1:]
#             tail=parts[2][last_slash_pos(parts[2])+1:]       
#             
#             tripleSet=head2tripleSet.get(head)
#             posi=(head, relation, tail)
#             count=0
#             if tripleSet is None: # no negative triples
#                 zero_nega+=1
#                 print head
#             else:
#                 if posi in tripleSet:
#                     tripleSet.remove(posi)
#                 if len(tripleSet)>0:
#                     write_SQ.write(head+' == '+relation+' == '+tail+'\t')
#                     count=len(tripleSet)
#                     for triple in tripleSet:
#                         if triple != posi:
#                             write_SQ.write(triple[0]+' == '+triple[1]+' == '+triple[2]+'\t')
#                     write_SQ.write(Q+'\n')
#             
#                     if count>max_triples:
#                         max_triples=count
#                     if count<min_triples:
#                         min_triples=count
#         read_SQ.close()
#         write_SQ.close()
#         print 'PNQ reformat over, max_nega_triples:', max_triples, 'min_nega_triples: ', min_triples, 'remove zero nega:', zero_nega   
#             
# def make_the_same_size_of_nega():
#     #remove those with no negative triples
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     files=['annotated_fb_data_train_PNQ', 'annotated_fb_data_test_PNQ', 'annotated_fb_data_valid_PNQ']  
#     nega_size=   5+2 # 50 nega and one posi, one question
#     for fil in files:
#         readfile=open(path+fil+'.txt', 'r')
#         writefile=open(path+fil+'_'+str(nega_size-2)+'nega.txt', 'w')
#         for line in readfile:
#             parts=line.strip().split('\t')
#             length=len(parts)
#             if length>2:
#                 if length<nega_size:
#                     repeat_triple=parts[-2]
#                     for triple in parts[:-1]:
#                         writefile.write(triple+'\t')
#                     for i in range(nega_size-length):
#                         writefile.write(repeat_triple+'\t')
# 
#                 else:
#                     for triple in parts[:nega_size-1]:
#                         writefile.write(triple+'\t')
# 
#                 writefile.write(parts[-1]+'\n')#question
#         writefile.close()
#         readfile.close()
#     print 'over'
# def    load_id2names():
#                 readfile=open('/mounts/data/corp/freebase.com/freebase.id2names', 'r')
#                 id2names={}
#                 count=0
#                 for    line    in    readfile:
#                                 parts=line.strip().split('::')
#                                 id2names[parts[0].strip()]=parts[1].strip().lower()
#                                 count+=1
#                                 #exit(0)
#                 print count, 'names, loaded over'
#                 readfile.close()
#                 return id2names
# def str2ngrams_list(strr, n):
#     char_list=list(strr)
#     length=len(char_list)
#     if length<n:
#         left=(n-length)/2
#         right=n-left-length
#         char_list=[' ']*left+char_list+[' ']*right
#         return [''.join(char_list)]
#     else:
#         return [''.join(char_list[i:(i+n)]) for i in range(len(char_list)-n+1)]
# def    load_id2names_id2des():
#     readfile=codecs.open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/freebase-subsets/freebase-FB2M-id2Name_20tokensDes.txt', 'r', 'utf-8')
#     id2names={}
#     id2des={}
#     count=0
#     for    line    in    readfile:
#         parts=line.strip().split('\t')
#         if len(parts)==3:
# 
#             name=parts[1].strip().lower()
#             des=parts[2].strip()
#             if des=='<None>':
#                 des=name
#             idd=parts[0].strip()
#             id2names[idd]=name
#             id2des[idd]=des.lower()
#                 
#             count+=1
# #             if count%100==0:
# #                 print count
#     print count, 'names, des, loaded over'
#     readfile.close()
#     return id2names, id2des  
# def    load_id2names_word2ids():
#                 readfile=codecs.open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/freebase-subsets/freebase-FB2M-id2NameDes.txt', 'r', 'utf-8')
#                 id2names={}
#                 word2ids={}
# #                 threegram2ids={}
# #                 fourgram2ids={}
# #                 fivegram2ids={}
# #                 mention2ids={}
#                 count=0
#                 for    line    in    readfile:
#                                 parts=line.strip().split('\t')
#                                 if len(parts)==3:
# 
#                                     name=parts[1].strip().lower()
# 
#                                     idd=parts[0].strip()
# #                                     for threegram in str2ngrams_list(name, 3):
# #                                         id_set_3=threegram2ids.get(threegram, set())
# #                                         id_set_3.add(idd)
# #                                         threegram2ids[threegram]=id_set_3
# #                                     for fourgram in str2ngrams_list(name, 4):
# #                                         id_set_4=fourgram2ids.get(fourgram, set())
# #                                         id_set_4.add(idd)
# #                                         fourgram2ids[fourgram]=id_set_4
# #                                     for fivegram in str2ngrams_list(name, 5):
# #                                         id_set_5=fivegram2ids.get(fivegram, set())
# #                                         id_set_5.add(idd)
# #                                         fivegram2ids[fivegram]=id_set_5
#                                     id2names[idd]=name
# #                                     id_set=mention2ids.get(name, set())
# #                                     id_set.add(idd)
# #                                     mention2ids[name]=id_set
#                                     for word in name.split():
#                                         MIDSet=word2ids.get(word, set())
#                                         MIDSet.add(idd)
#                                         word2ids[word]=MIDSet
#                                         
#                                     count+=1
# #                                     if count%100000==0:
# #                                         print 'loading id2names',count, '...'
#                                 #exit(0)
#                 print count, 'names, loaded over'
#                 readfile.close()
#                 return id2names, word2ids  
# def    load_id2names_word2ids_3gram2ids_4gram2ids_5gram2ids_mention2ids():
#                 readfile=codecs.open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/freebase-subsets/freebase-FB2M-id2NameDes.txt', 'r', 'utf-8')
#                 id2names={}
#                 word2ids={}
#                 threegram2ids={}
#                 fourgram2ids={}
#                 fivegram2ids={}
#                 mention2ids={}
#                 count=0
#                 for    line    in    readfile:
#                                 parts=line.strip().split('\t')
#                                 if len(parts)==3:
# 
#                                     name=parts[1].strip().lower()
# 
#                                     idd=parts[0].strip()
#                                     for threegram in str2ngrams_list(name, 3):
#                                         id_set_3=threegram2ids.get(threegram, set())
#                                         id_set_3.add(idd)
#                                         threegram2ids[threegram]=id_set_3
#                                     for fourgram in str2ngrams_list(name, 4):
#                                         id_set_4=fourgram2ids.get(fourgram, set())
#                                         id_set_4.add(idd)
#                                         fourgram2ids[fourgram]=id_set_4
#                                     for fivegram in str2ngrams_list(name, 5):
#                                         id_set_5=fivegram2ids.get(fivegram, set())
#                                         id_set_5.add(idd)
#                                         fivegram2ids[fivegram]=id_set_5
#                                     id2names[idd]=name
#                                     id_set=mention2ids.get(name, set())
#                                     id_set.add(idd)
#                                     mention2ids[name]=id_set
#                                     for word in name.split():
#                                         MIDSet=word2ids.get(word, set())
#                                         MIDSet.add(idd)
#                                         word2ids[word]=MIDSet
#                                         
#                                     count+=1
# #                                     if count%100000==0:
# #                                         print 'loading id2names',count, '...'
#                                 #exit(0)
#                 print count, 'names, loaded over'
#                 readfile.close()
#                 return id2names, word2ids , threegram2ids, fourgram2ids, fivegram2ids, mention2ids           
# def create_id_to_name_des_types():
#     id2names=load_id2names()
#     id2des=entity_description_statistics()
#     id2types=load_id2types()
#     ids=set(id2names.keys())|set(id2des.keys())|set(id2types.keys())
#     writefile=gzip.open('/mounts/data/proj/wenpeng/Dataset/freebase/id_to_name_des_types.txt.gz', 'w')
#     
#     for id in ids:
#         types=id2types.get(id, '<None>')
#         name=id2names.get(id, '<None>')
#         des=id2des.get(id, '<None>')
#         writefile.write(id+'\t'+name+'\t'+des)
#         for type in types:
#             writefile.write('\t'+type)
#         writefile.write('\n')
#     writefile.close()
#     print 'create_id_to_name_des_types store over.'
# 
# def load_id2types():
#     readfile=open('/mounts/data/corp/freebase.com/freebase.id2types', 'r')
#     id2types={}
#     discard_type='common.topic'
#     for line in readfile:
#         parts=line.strip().split('::')
#         types=set()
#         id=parts[0].strip()
#         for part in parts[1:]:
#             part=part.strip()
#             types.add(part[last_slash_pos(part)+1:])
# #             print types
# #             exit(0)
#         if len(types)>1 and discard_type in types:
#             types.discard(discard_type)
#         id2types[id]=types
#             
#     print 'types store over.'
#     readfile.close()
#     return id2types    
#     
#     
# def load_id2notabletypes():
#     readfile=gzip.open('/mounts/data/corp/freebase.com/freebase-rdf-2014-04-13-00-00.gz', 'r')
#     id2notabletype={}
#     
#     for line in readfile:
#         parts=line.strip().split()
#         if parts[0].find('/m.')>0 and parts[1].find('/type.object.type')>0:
#             id=parts[0][last_slash_pos(parts[0].strip())+1:-1]
#             type=parts[2][last_slash_pos(parts[2].strip())+1:-1]
#             id2notabletype[id]=type
#     print 'notable typle store over.'
#     readfile.close()
#     return id2notabletype
# 
# def entity_description_tokenize():
#     des_file=gzip.open('/mounts/data/proj/wenpeng/Dataset/freebase/Heike_id2des.txt.gz', 'r')
#     write_file= gzip.open('/mounts/data/proj/wenpeng/Dataset/freebase/Heike_id2des_tokenized.txt.gz', 'w')    
#     for line in des_file:
#         parts=line.strip().split('\t')
#         if len(parts)==2:
#             tokenized_des=nltk.word_tokenize(parts[1].strip().lower().decode('utf-8'))
#             write_file.write(parts[0].strip()+'\t'+' '.join([x.encode('utf-8') for x in tokenized_des])+'\n')
#     write_file.close()
#     des_file.close()
#     
# def entity_description_statistics():
#     #first load all descriptions
#     des_file=gzip.open('/mounts/data/proj/wenpeng/Dataset/freebase/Heike_id2des_tokenized.txt.gz', 'r')
#     id2des={}
#     for line in des_file:
# 
#         parts=line.strip().split('\t')
#         if len(parts)==2:
#             id2des[parts[0].strip()]=parts[1].strip().lower()
#     des_file.close()
#     print 'totally id2des size:', len(id2des)
#     return id2des
# def idList2StrDndDes(ids, id2names, id2des):
#     strList=[]
#     desList=[]
#     for id in ids:
#         str=id2names.get(id)
#         if str is None:
#             str=id
#         des=id2des.get(id)
#         if des is None:
#             des=str     
#         strList.append(str)
#         desList.append(des)
#     return strList, desList
#     
# 
# def MID2str_str2des():
#     #first load MID2str, and str to des
#     nega_size=5
#     id2names=load_id2names()
#     id2des=entity_description_statistics()
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     files=['annotated_fb_data_train_PNQ_'+str(nega_size)+'nega', 'annotated_fb_data_test_PNQ_'+str(nega_size)+'nega', 'annotated_fb_data_valid_PNQ_'+str(nega_size)+'nega']      
#     for fil in files:
#         readfile=open(path+fil+'.txt', 'r')
#         writefile=open(path+fil+'_str&des.txt', 'w')
#         for line in readfile:
#             parts=line.strip().split('\t')
# 
#             ids=[]
# 
#             for i in range(nega_size+1): #1 posi, 50 nega
#                 ids.append('m.'+parts[i].split(' == ')[0].strip())
#                 ids.append('m.'+parts[i].split(' == ')[2].strip())
#             strList, desList=idList2StrDndDes(ids, id2names, id2des) #52
#             for i in range(len(parts[:-1])):#51
#                 units=parts[i].split(' == ')
#                 relation=units[1]
#                 writefile.write(strList[i*2]+' == '+relation+' == '+strList[i*2+1]+'\t')
#             for des in desList: #52, 1 head, 51 tail
#                 writefile.write(des+'\t')
#             writefile.write(parts[-1]+'\n')
#         writefile.close()
#         readfile.close()
#         print fil, '..finished'
#             
# def freebase_id2des():
#     readfile=gzip.open('/mounts/data/corp/freebase.com/freebase.descriptions.gz', 'r')
#     writefile=gzip.open('/mounts/data/proj/wenpeng/Dataset/freebase/Heike_id2des.txt.gz', 'w')
#     for line in readfile:
#         if line.strip().find('@en')>=0:
# #             print line
# #             exit(0)
#             parts=line.strip().split('\t')
#             id= parts[0][last_slash_pos(parts[0])+1:-1]
#             posi=parts[2].find('"')
#             rposi=parts[2].rfind('"')
#             des= parts[2][posi+1:rposi]
#             writefile.write(id+'\t'+des+'\n')
#     writefile.close()
#     readfile.close()
#     print 'id2des over'                   
# 
# def ungroup_FB2M5M():
#     read5M=open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/freebase-subsets/freebase-FB5M.txt', 'r')
#     write5M=open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/freebase-subsets/freebase-FB5M-ungrouped.txt', 'w')
#     fb5M=set()
#     for line in read5M:
#         parts=line.strip().split()
#         size=len(parts)-2
#         for i in range(size):
#             new_triple=parts[0]+'\t'+parts[1]+'\t'+parts[i]
#             if  new_triple not in fb5M and parts[i].find('/m/')>=0:
#                 fb5M.add(new_triple)
#                 write5M.write(new_triple+'\n')
#     write5M.close()
#     read5M.close()
#     print 'ungroup finished'
# 
# def check_if_fb5M_contains_fb2M():
#     read5M=open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/freebase-subsets/freebase-FB5M-ungrouped.txt', 'r')
#     fb5M_entity=set()
#     fb5M_relation=set()
#     for line in read5M:
#         parts=line.strip().split()
#         fb5M_entity.add(parts[0])
#         fb5M_entity.add(parts[2])
#         fb5M_relation.add(parts[1])
#     read5M.close()
#     print '5M loaded over'
#     read2M=open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/freebase-subsets/freebase-FB2M-ungrouped.txt', 'r')
#     e_co=0
#     r_co=0
#     for line in read2M:
#         parts=line.strip().split()
#         if parts[0] not in fb5M_entity:
#             e_co+=1
#         if parts[2] not in fb5M_entity:
#             e_co+=1
#         if parts[1] not in fb5M_relation:
#             r_co+=1
#     read2M.close()
#     print e_co, r_co
# 
# def combine_fb2M_fb5M():
#     read5M=open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/freebase-subsets/freebase-FB5M-ungrouped.txt', 'r')
#     writefile=open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/freebase-subsets/freebase-FB5M2M-combined.txt', 'w')
#     fb5M=set()
# 
#     for line in read5M:
#         writefile.write(line.strip()+'\n')
#         fb5M.add(line.strip())
#     read5M.close()
#     print '5M loaded over'
#     read2M=open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/freebase-subsets/freebase-FB2M-ungrouped.txt', 'r')
# 
#     for line in read2M:
#         if line.strip() not in fb5M:
#             writefile.write(line.strip()+'\n')
#     read2M.close()
#     print 'over'
# 
# 
# 
# def split_Questions_into_mention_remainQ():
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     infile=['annotated_fb_data_train_PNQ_50nega_str&des.txt', 'annotated_fb_data_valid_PNQ_50nega_str&des.txt', 'annotated_fb_data_test_PNQ_50nega_str&des.txt']
#     outfile=['annotated_fb_data_train_mention_remainQ.txt', 'annotated_fb_data_valid_mention_remainQ.txt', 'annotated_fb_data_test_mention_remainQ.txt']
#     exclude= set(string.punctuation)
#     for i in range(3):
#         readfile=codecs.open(path+infile[i], 'r', 'utf-8')
#         writefile=codecs.open(path+outfile[i], 'w', 'utf-8')
#         line_co=0
#         for line in readfile:
#             mention=''
#             
#             parts=line.strip().split('\t')
#             pos_triple=parts[0]
#             head=pos_triple.strip().split(' == ')[0].strip().lower()
#             raw_Q=parts[-1].lower()
#             Q=nltk.word_tokenize(raw_Q.strip())
#             Q_words=set(Q)
#             
#             remainQ=Q
# #             print 'raw_Q', raw_Q
# #             print 'Q', Q
# 
#             head_words=head.split()
#             for head_word in head_words:
#                 if head_word in Q_words:
#                     mention+=' '+head_word
# #                     print 'head_word:', head_word, 'remainQ:', remainQ
#                     Q_words.discard(head_word)
#                     remainQ.remove(head_word)
#             if remainQ[-1] in exclude:
#                 remainQ=remainQ[:-1]     
#             if len(mention.strip())==0:
#                 mention=head
# #                 exit(0)        
# #             print head, raw_Q, mention, remainQ
#             writefile.write(head+'\t'+raw_Q+'\t'+mention.strip()+'\t'+' '.join(remainQ)+'\n')
#         readfile.close()
#         writefile.close()
#         print i, 'finished'
#                     
#             
#             
#             
# def extract_questions():
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     files=['annotated_fb_data_train', 'annotated_fb_data_test', 'annotated_fb_data_valid']      
#     for fil in files:   
#         print fil, '...'
#         readfile=open(path+fil+'.txt', 'r')
#         writefile=open(path+fil+'.questions.txt', 'w')
#         for line in readfile:
#             parts=line.strip().split('\t')
#             writefile.write(parts[-1]+'\n')
#         readfile.close()
#         writefile.close()
#     print 'finished'           
# 
# 
# def convert_stanfordPOSFile_into_TokenizedFile():
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     stanford=['annotated_fb_data_train.questions', 'annotated_fb_data_test.questions', 'annotated_fb_data_valid.questions']    
#     for fil in stanford:
#         print fil, '...'
#         open_standford=codecs.open(path+fil+'_stanfordPOS.txt', 'r', 'utf-8')
# 
#         writefile=codecs.open(path+fil+'_stanfordTokenized.txt', 'w', 'utf-8')
#         lin_co=0   
#         for line in open_standford:
#             parts=line.strip().split()
#             new_sent=[]
#             for part in parts:
#                 pos=part.rfind('_')
#                 if pos>0:
#                     new_sent.append(part[:pos])
#                 else:
#                     print lin_co, 'wrong tokenized:', part, line
#                     exit(0)
#             writefile.write(' '.join(new_sent)+'\n')
#             lin_co+=1
#         writefile.close()
#         open_standford.close()
#     print 'over' 
# 
# def nltk_POSTagging():
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     files=['annotated_fb_data_train.questions', 'annotated_fb_data_test.questions', 'annotated_fb_data_valid.questions']
#     for fil in files:    
#         print fil, '...'
#         f=codecs.open(path+fil+'_stanfordTokenized.txt', 'r', 'utf-8')
#         wfile=codecs.open(path+fil+'_nltkPOS.txt', 'w', 'utf-8')
#         for line in f:
# #             print line.strip()
#             tagged_sentence=nltk.pos_tag(line.strip().split())
#             line=''
#             for (word, tag) in tagged_sentence:
#                 line+=' '+word+'_'+tag
#             wfile.write(line.strip()+'\n')
#         wfile.close()
#         f.close()
#     print 'nltk pos tagging over.'
# 
# def parse_flors(fil):
#     readfile=codecs.open(fil, 'r', 'utf-8')
#     words=[]
#     tags=[]
#     for line in readfile:
#         line=line.strip()
#         if len(line)>0:
#             parts=line.split()
#             words.append(parts[0])
#             tags.append(parts[1])
#     readfile.close()
#     return words, tags
# 
# def parse_stanfordPOS_or_nltkPOS(fil):
#     readfile=codecs.open(fil, 'r', 'utf-8')
#     words=[]
#     tags=[]
#     count=0
#     for line in readfile:
#         parts=line.strip().split()
#         for part in parts:
#             pos=part.rfind('_')
#             if pos>=0:
#                 words.append(part[:pos])
#                 tags.append(part[pos+1:])
#             else:
#                 words.append(part.strip())
#                 tags.append('<OOV>')
#         count+=1
#     readfile.close()
#     
#     return words, tags   
# def sentence_lengths(fil):
#     lengths=[]
#     readfile=codecs.open(fil, 'r', 'utf-8')
#     for line in readfile:
#         lengths.append(len(line.strip().split()))
#     readfile.close()
#     return lengths
# def combine_three_POStags():
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     flors=['annotated_fb_data_train.questions_florsPOS.txt', 'annotated_fb_data_test.questions_florsPOS.txt', 'annotated_fb_data_valid.questions_florsPOS.txt']   
#     nltk=['annotated_fb_data_train.questions_nltkPOS.txt', 'annotated_fb_data_test.questions_nltkPOS.txt', 'annotated_fb_data_valid.questions_nltkPOS.txt'] 
#     stanford=['annotated_fb_data_train.questions_stanfordPOS.txt', 'annotated_fb_data_test.questions_stanfordPOS.txt', 'annotated_fb_data_valid.questions_stanfordPOS.txt']
#     
#     
#     for i in range(3):
#         open_flors=codecs.open(path+flors[i], 'r', 'utf-8')
#         open_nltk=codecs.open(path+nltk[i], 'r', 'utf-8')
#         open_standford=codecs.open(path+stanford[i], 'r', 'utf-8')
#         if i==0:
#             writefile=codecs.open(path+'annotated_fb_data_train.questions_combinedPOS.txt', 'w', 'utf-8')
#         elif i==1:
#             writefile=codecs.open(path+'annotated_fb_data_test.questions_combinedPOS.txt', 'w', 'utf-8')
#         else:
#             writefile=codecs.open(path+'annotated_fb_data_valid.questions_combinedPOS.txt', 'w', 'utf-8')
#             
#         sent_lengths=sentence_lengths(path+nltk[i])
#         flors_words, flors_tags=parse_flors(path+flors[i])
#         nltk_words, nltk_tags=parse_stanfordPOS_or_nltkPOS(path+nltk[i])        
#         stanford_words, stanford_tags=parse_stanfordPOS_or_nltkPOS(path+stanford[i])
# 
#         sent_size=len(flors_words)
#         if sent_size!=len(nltk_words) or sent_size!=len(stanford_words):
#             print 'size not equal'
#             print sent_size, len(nltk_words), len(stanford_words)
#             print set(stanford_words)-set(nltk_words)
#             exit(0)
# #         else:
#         sum_length=0
#         sent_index=0
#         wrong=0
#         for i in sent_lengths:
#             
#             for j in range(sum_length, sum_length+i):
#                     
#                 new_tags=''
# 
#                 if flors_tags[j]==nltk_tags[j] or flors_tags[j]==stanford_tags[j]:
#                     new_tags=flors_tags[j]
#                 else:
#                     new_tags=stanford_tags[j]
#                 if flors_words[j]!=stanford_words[j]:
#                     print sent_index, j, flors_words[j],':', stanford_words[j]
#                     wrong+=1
#                     if wrong==40:
#                         exit(0)
# #                     exit(0)
#                 
#                 writefile.write(flors_words[j]+'_'+new_tags+' ')
#             writefile.write('\n')
#             sum_length+=i
#             sent_index+=1
#         writefile.close()
#         open_flors.close()
#         open_nltk.close()
#         open_standford.close()
#     print 'POS tags combined over.'
# # def load_postagged_questions():
# 
# def wordPOS_to_wordlabel(wordPOS):
#     initial_indicators={'NN', 'NNS', 'NNP', 'NNPS', 'FW'}
#     wh_indicators={'WP', 'WDT'}
#     pre_pos='empty'
#     wordlabel=[]
#     for part in wordPOS:
#         splitt=part.find('_')
#         word=part[:splitt]
#         pos=part[splitt+1:]
#         if pos      in initial_indicators and pre_pos not in wh_indicators:
#             wordlabel.append(word+'_'+str(1))
#         else:
#             wordlabel.append(word+'_'+str(0))
#         pre_pos=pos
#     return wordlabel
# def refine_wordPOS_wordlabel(wordpos, wordlabel):
#     refined_pos={'JJ', 'CD'}
# #     print 'wordpos:', wordpos
# #     print 'wordlabel:', wordlabel
#     for i in range(len(wordlabel)-1):
#         if wordpos[i].split('_')[1] in refined_pos and wordlabel[i+1].split('_')[1]=='1':
#             wordlabel[i]=wordpos[i].split('_')[0]+'_'+str(1)
#     return wordlabel
#         
# 
# def extract_mention_candidates(refined_wordlabel):
#     candidates=[]
#     refined_wordlabel=refined_wordlabel[::-1]
#     cand=''
#     for ele in    refined_wordlabel:
#         parts=ele.split('_')
#         if parts[1]=='1':           
#             cand=parts[0]+' '+cand
#         if parts[1]=='0' and len(cand)>0:
#             candidates.append(cand.strip().lower())
#             cand=''
#     return candidates
# def mention2IDs(mention, word2ids, mention2ids):
#     ids=[]
#     existed_idset=mention2ids.get(mention)
#     if existed_idset is not None:
#         ids+=list(existed_idset)
# 
#     words=mention.split()
#     id_times={}
#     word_ids_list=[]
#     for word in words:
#         word_ids=word2ids.get(word)
#         if word_ids is not None:
#             word_ids_list.append(word_ids)
#     word_ids_union=set()
#     for subset in word_ids_list:
#         word_ids_union=word_ids_union|subset
#     for ind_id in word_ids_union:
#         count=0
#         for subset in word_ids_list:
#             if ind_id in subset:
#                 count+=1
#         id_times[ind_id]=count
#     
#     sorted_id_times=sorted(id_times.items(), key=operator.itemgetter(1), reverse=True)  
# #         ids|=  set( [entry[0] for entry in  sorted_id_times[:2] ] )
#     ids+=  [entry[0] for entry in  sorted_id_times] 
#     return ids  
# 
# 
# def remove_noisestr(question, overall_ids, id2names):
# #     print 'question:', question
#     orig_overall_ids=overall_ids[:]
#     removed_ids=[]
#     for id in overall_ids:
#         name=id2names.get(id)
# #         print 'name:', name
#         for word in name.split():
#             if word not in question:
#                 removed_ids.append(id)
#                 break
# #     print 'overall_ids:', overall_ids
# #     print 'removed_ids:', removed_ids
#     for id in removed_ids:
#         overall_ids.remove(id)
# #     if len(overall_ids)==0:
# #         return orig_overall_ids
# #     else:
# #         return overall_ids    
#     return overall_ids
# 
# def lcsubstring_length(a, b):
#     
#     len_a=len(a)
#     len_b=len(b)
#     a_label=[0]*len_a
#     table=[[0]*(len_b+1) for _ in xrange(len_a+1)]
#     l=0
#     for i, ca in enumerate(a,1):
#         for j, cb in enumerate(b,1):
#             if ca==cb:
#                 table[i][j]=table[i-1][j-1]+1
#                 if table[i][j]>l:
#                     l=table[i][j]
#                     a_label[i-1]=1
# 
#     
# #     left=-1
# #     for ind, value in enumerate(a_label):
# #         if value ==1:
# #             left=ind+1
# #             break
#     right=-1
#     for ind, value in enumerate(a_label[::-1]):
#         if value ==1:
#             right=ind
#             break
#     right=len_a-right
#     middle=(0+right)/2
# #     start=-1
# #     for ind, value in enumerate(a_label[::-1]):
# #         if value ==1:
# #             start=ind+1
# #             break
# #     posi_importance=(len_a-start)*1.0/len_a
#     posi_importance=middle*1.0/len_a
#     simi_1=l*1.0/len_b
#     simi_2=l*0.6/len_a
#     simi_3=0.1*posi_importance
#     return simi_1+simi_2+simi_3, simi_1, simi_2, simi_3 
#                     
# 
# def substringRato(list1, list2):
#     cover=0
#     list1_set=set(list1)
#     for ele in list2:
#         if ele in list1_set:
#             cover+=1
# #     overall_size=len(list2)
# #     cover=overall_size-len(set(list2)-set(list1))
#     return cover*1.0/len(list2)
# 
# def ranking_ids_topN(question_list, interset_id_set_w345, id2names, N):
#     id2score={}
#     id2simi_1={}
#     id2simi_2={}
#     id2simi_3={}
# #     weights=[0.4, 0.15, 0.2, 0.25]
#     for idd in interset_id_set_w345:
#         name=id2names.get(idd)
# #         print 'name:', name
#         name_words=name.split()
# #         threegram_querys=str2ngrams_list(name, 3)
# #         fourgram_querys=str2ngrams_list(name, 4)
# #         fivegram_querys=str2ngrams_list(name, 5)    
#         overall_simi, simi_1, simi_2, simi_3=lcsubstring_length(question_list, name_words)
#         id2score[idd]=overall_simi
#         id2simi_1[idd]=simi_1
#         id2simi_2[idd]=simi_2
#         id2simi_3[idd]=simi_3
# #         print 'question_list:', question_list
# #         print 'name:', name
# #         print 'scores:', word_simi, three_simi, four_simi, five_simi, overall_simi
# #         if idd=='m.04whkz5':
# #             exit(0)
#     sorted_map=sorted(id2score.items(), key=operator.itemgetter(1), reverse=True)[:N]
# #     sorted_map=heapq.nlargest(N, id2score.items(), key=itemgetter(1))
#     top_N_ids=[]
#     top_id2simi={}
#     top_id2simi_1={}
#     top_id2simi_2={}
#     top_id2simi_3={}
#     for tup in sorted_map:
#         idd=tup[0]
#         top_N_ids.append(idd)
#         top_id2simi[idd]=tup[1]
#         top_id2simi_1[idd]=id2simi_1.get(idd)
#         top_id2simi_2[idd]=id2simi_2.get(idd)
#         top_id2simi_3[idd]=id2simi_3.get(idd)
#     return top_N_ids, top_id2simi, top_id2simi_1, top_id2simi_2, top_id2simi_3, id2score, id2simi_1, id2simi_2, id2simi_3
# def load_gold_head_ids(infile):
#     readfile=codecs.open(infile, 'r', 'utf-8')        
#     id_list=[]
#     for line in readfile:
#         parts=line.strip().split('\t')
#         id='m.'+parts[0][last_slash_pos(parts[0])+1:]
#         id_list.append(id)
#     readfile.close()
#     return id_list
# 
# def truncate_train_35000toEnd():
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     readfile=codecs.open(path+'annotated_fb_data_train.txt', 'r', 'utf-8')
#     writefile=codecs.open(path+'annotated_fb_data_train_35000toEnd.txt', 'w', 'utf-8')
#     line_co=0
#     for line in readfile:
#         if line_co<35000:
#             line_co+=1
#             continue
#         else:
#             writefile.write(line.strip()+'\n')
#             line_co+=1
# 
# 
#     readfile.close()
#     writefile.close()
#     print 'training file truncate 35000 finished'
# def FB2M_SimpleQA_EntityLinking():
# #     id2names, word2ids, threegram2ids, fourgram2ids, fivegram2ids, mention2ids=    load_id2names_word2ids_3gram2ids_4gram2ids_5gram2ids_mention2ids()
#     N=100
# #     postag_imp={'NN':1, 'NNS':1, 'NNP':1, 'NNPS':1, 'FW':1, 'WP':0, 'WDT':0, 'JJ':0.5, 'CD':0.8}
#     
#     id2names, word2ids=    load_id2names_word2ids()
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     files=['annotated_fb_data_test.questions_stanfordTokenized.txt', 'annotated_fb_data_valid.questions_stanfordTokenized.txt', 'annotated_fb_data_train.questions_stanfordTokenized.txt']   
# #     files=['annotated_fb_data_train.questions_stanfordTokenized.txt']
#     q_files=['annotated_fb_data_test.txt', 'annotated_fb_data_valid.txt', 'annotated_fb_data_train.txt']
# #     q_files=['annotated_fb_data_train.txt']
#     for i in range(2):
#         print i, '...'
#         readfile=codecs.open(path+files[i], 'r', 'utf-8')
# #         if i==0:
# #             writefile=codecs.open(path+'annotated_fb_data_test.entitylinking.top'+str(N)+'.FB2M.newFormat.txt', 'w', 'utf-8')
# #         elif i==1:
# #             writefile=codecs.open(path+'annotated_fb_data_valid.entitylinking.top'+str(N)+'.FB2M.newFormat.txt', 'w', 'utf-8')
# 
#         gold_id_list=load_gold_head_ids(path+q_files[i])
#         line_co=0
# #         example_size=len(gold_id_list)
#         succ_size=0
#         top1=0
#         top5=0
#         top10=0
#         top20=0
#         top50=0
# #         sum_cand_size=0
#         uncover_size=0
#         start_time = time.clock()
#         for line in readfile:
#             question=line.strip().lower()
#             question_list=question.split()
# #                 postag=part.split('_')[1]
# #                 question_pos_list.append(postag_imp.get(postag, 0.0))
# #             question_str=' '.join(question_list)
# #             raw_wordlabel=wordPOS_to_wordlabel(parts)
# #             refined_wordlabel=refine_wordPOS_wordlabel(parts, raw_wordlabel)
# #             men_cands=extract_mention_candidates(refined_wordlabel)
# #             if len(men_cands)==0:
# #                 print 'zero mentions:', line
# #             men_cands=[' '.join([wordpos.split('_')[0] for wordpos in parts])]       
# #             threegram_mens=str2ngrams_list(question_str, 3)
# #             fourgram_mens=str2ngrams_list(question_str, 4)
# #             fivegram_mens=str2ngrams_list(question_str, 5)
#             overall_ids=set()
# #             word_id_set=set()
#             for word in question_list:
#                 word_ids=  word2ids.get(word, set())  
#                 overall_ids|=word_ids
# 
#             if len(overall_ids)==0:
#                 uncover_size+=1
#                 line_co+=1
#                 continue
#             top_N_ids, top_id2simi, top_id2simi_1, top_id2simi_2, top_id2simi_3, all_id2score, all_id2simi_1, all_id2simi_2, all_id2simi_3=ranking_ids_topN(question_list, overall_ids, id2names, N)
#             gold_mid=gold_id_list[line_co]
#             
#             
#             if i==0 or i==1:
#                 gold_position=N
#                 if gold_mid in set(top_N_ids):
#                     succ_size+=1
#                     gold_position=top_N_ids.index(gold_mid)
#                     if gold_position==0:
#                         top1+=1
#                     if gold_position<5:
#                         top5+=1
#                     if gold_position<10:
#                         top10+=1
#                     if gold_position<20:
#                         top20+=1
#                     if gold_position<50:
#                         top50+=1
# #                     top_N_ids.remove(gold_mid)
# #                 writefile.write(str(gold_position)\
# #                                     +'\t'+'\t'.join([idd+'=='+str(top_id2simi.get(idd))+'=='+str(top_id2simi_1.get(idd))+'=='+str(top_id2simi_2.get(idd))+'=='+str(top_id2simi_3.get(idd)) for idd in top_N_ids])+'\t'+question+'\n')
# #                     
# 
# #                     writefile.write('0\t'+'\t'.join([idd+'=='+str(top_id2simi.get(idd))+'=='+str(top_id2simi_1.get(idd))+'=='+str(top_id2simi_2.get(idd))+'=='+str(top_id2simi_3.get(idd)) for idd in top_N_ids])+'\t'+question+'\n')
#             else:
#                 if gold_mid in set(top_N_ids):
#                     succ_size+=1
#                     if gold_mid==top_N_ids[0]:
#                         top1+=1
#                     top_N_ids.remove(gold_mid)
#                 else:
#                     top_N_ids=top_N_ids[:-1]
#                     
# #                 writefile.write(gold_mid+'=='+str(all_id2score.get(gold_mid))+'=='+str(all_id2simi_1.get(gold_mid))+'=='+str(all_id2simi_2.get(gold_mid))+'=='+str(all_id2simi_3.get(gold_mid))\
# #                                     +'\t'+'\t'.join([idd+'=='+str(top_id2simi.get(idd))+'=='+str(top_id2simi_1.get(idd))+'=='+str(top_id2simi_2.get(idd))+'=='+str(top_id2simi_3.get(idd)) for idd in top_N_ids])+'\t'+question+'\n')
# #                                  
#             line_co+=1
#             
#             if line_co%1000==0:
#                 print line_co, 'top1:', top1*1.0/line_co,'top5:', top5*1.0/line_co,'top10:', top10*1.0/line_co,'top20:', top20*1.0/line_co,'top50:', top50*1.0/line_co,'top100:', succ_size*1.0/line_co#, 'uncover_size:',uncover_size,         'uses ', (time.clock()-start_time)/60.0, 'min'
# 
# #             if line_co==6:
# #                 exit(0)
#         readfile.close() 
# #         writefile.close()
# #         exit(0)
#         
# def FB2M_id2str_id2des():
#     #first load how many ids in FB2M
#     readfile=open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/freebase-subsets/freebase-FB5M-ungrouped.txt', 'r')
#     FB_ids=set()
#     for line in readfile:
#         parts=line.strip().split()
#         head='m.'+parts[0][last_slash_pos(parts[0])+1:]
# #         relation=parts[1][last_slash_pos(parts[1])+1:]
#         tail='m.'+parts[2][last_slash_pos(parts[2])+1:]
#         FB_ids.add(head)
#         FB_ids.add(tail)       
#     readfile.close()
#     print 'freebase-FB5M-ungrouped.txt loaded over'
#     readfile=gzip.open('/mounts/data/proj/wenpeng/Dataset/freebase/id_to_name_des_types.txt.gz', 'r')   
#     writefile=open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/freebase-subsets/freebase-FB5M-id2NameDes.txt', 'w')    
#     for line in readfile:
#         parts=line.strip().split('\t')
#         id=parts[0]
#         name=parts[1]
#         des=parts[2]
#         if id in  FB_ids:
#             writefile.write(id+'\t'+' '.join(nltk.word_tokenize(name.decode('utf-8'))).encode('utf-8')+'\t'+des+'\n')
#     readfile.close()
#     writefile.close()  
#     print  'FB5M_id2str_id2des, finished'
# 
# def tokenize_id2NameDes():
#     readfile=codecs.open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/freebase-subsets/freebase-FB2M-id2NameDes.txt', 'r', 'utf-8')
#     writefile=codecs.open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/freebase-subsets/freebase-FB2M-id2Name_20tokensDes.txt', 'w', 'utf-8')    
#     empty_line=0
#     line_co=0
#     for line in readfile:
# #         line_co+=1
# #         print line_co        
#         parts=line.strip().split('\t')
#         if len(parts)!=3:
#             print line
#             empty_line+=1
#             continue
#         id=parts[0]
#         name=parts[1]
#         des=parts[2]
#         if des!='<None>':
#             des=' '.join(nltk.word_tokenize(des)[:20])
#         writefile.write(id+'\t'+name+'\t'+des+'\n')
# 
#     readfile.close()
#     writefile.close()  
#     print  'tokenized FB2M_id2str_id2des, finished, empty line:', empty_line
# 
# def HowMany_GroundTruthMID_HaveName():
#     id2names, word2ids=    load_id2names_word2ids()
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     files=['annotated_fb_data_train', 'annotated_fb_data_test', 'annotated_fb_data_valid']   
#     fail_no=0   
#     all_co=0
#     for fil in files:   
#         print fil, '...'
#         readfile=open(path+fil+'.txt', 'r')
#         for line in readfile:
#             parts=line.strip().split('\t')
#             head_id='m.'+parts[0][last_slash_pos(parts[0])+1:]
#             if id2names.get(head_id) is None:
#                 fail_no+=1
#                 print parts[0], parts[-1]
#             all_co+=1
#         readfile.close()
# 
#         print 'finished, fail:', fail_no, 'all no:', all_co   
#         fail_no=0
#         all_co=0   
# 
# def Remove_EntityLinkingFailed_TestValid():
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     test_valid=['annotated_fb_data_test.entitylinking.top20.txt', 'annotated_fb_data_valid.entitylinking.top20.txt']
#      
#     for i in range(2):
#         readfile=codecs.open(path+test_valid[i], 'r', 'utf-8')
#         if i==0:
#             writefile=codecs.open(path+'annotated_fb_data_test.entitylinking.top20_succSet.txt', 'w', 'utf-8')
#         else:
#             writefile=codecs.open(path+'annotated_fb_data_valid.entitylinking.top20_succSet.txt', 'w', 'utf-8')
#         for line in readfile:
#             parts=line.strip().split('\t')
#             if parts[0]=='1':
#                 writefile.write('\t'.join(parts[1:])+'\n')
#         writefile.close()
#         readfile.close()
#         print 'remove failed over'
# 
# def filter_test_valid_by_unentitylinked():
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     test_valid=['annotated_fb_data_test.entitylinking.top20.txt', 'annotated_fb_data_valid.entitylinking.top20.txt']
#     raw_test_valid=['annotated_fb_data_test.txt', 'annotated_fb_data_valid.txt']
#     for i in range(2):
#         label_list=[]
#         readfile=codecs.open(path+test_valid[i], 'r', 'utf-8')
#         for line in readfile:
#             parts=line.strip().split('\t')
#             if parts[0]=='1':
#                 label_list.append(1)
#             else:
#                 label_list.append(0)
#         readfile.close()
#         readfile=codecs.open(path+raw_test_valid[i], 'r', 'utf-8')
#         if i==0:
#             writefile=codecs.open(path+'annotated_fb_data_test_succSet.txt', 'w', 'utf-8')
#         else:
#             writefile=codecs.open(path+'annotated_fb_data_valid_succSet.txt', 'w', 'utf-8')
#         
#         count=0
#         for line in readfile:
#             if label_list[count]==1:
#                 writefile.write(line.strip()+'\n')
#             count+=1
#         readfile.close()
#         writefile.close()
#         print 'remove raw test_valid failed over'    
# def filter_test_valid_fixMention_by_unentitylinked():
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     test_valid=['annotated_fb_data_test.entitylinking.top20.txt', 'annotated_fb_data_valid.entitylinking.top20.txt']
#     raw_test_valid=['annotated_fb_data_test.questions_fixedMentions_goldEntity.txt', 'annotated_fb_data_valid.questions_fixedMentions_goldEntity.txt']
#     
#     for i in range(2):
#         label_list=[]
#         readfile=codecs.open(path+test_valid[i], 'r', 'utf-8')
#         for line in readfile:
#             parts=line.strip().split('\t')
#             if parts[0]=='1':
#                 label_list.append(1)
#             else:
#                 label_list.append(0)
#         readfile.close()
#         readfile=codecs.open(path+raw_test_valid[i], 'r', 'utf-8')
#         if i==0:
#             writefile=codecs.open(path+'annotated_fb_data_test_Q_fixMention_succSet.txt', 'w', 'utf-8')
#         else:
#             writefile=codecs.open(path+'annotated_fb_data_valid_Q_fixMention_succSet.txt', 'w', 'utf-8')
#         
#         count=0
#         for line in readfile:
#             if label_list[count]==1:
#                 writefile.write(line.strip()+'\n')
#             count+=1
#         readfile.close()
#         writefile.close()
#         print 'remove fixMention test_valid failed over'  
# def load_id2tuples():
#     read5M=codecs.open('/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/freebase-subsets/freebase-FB2M-ungrouped.txt', 'r', 'utf-8')
#     id2tuples={}
#     count=0
#     for line in read5M:
#         parts=line.strip().split()
#         idd='m.'+parts[0][last_slash_pos(parts[0])+1:]
#         relation=parts[1][last_slash_pos(parts[1])+1:]
#         
#         tup=(idd, relation)
#         id_tup=id2tuples.get(idd)
#         if id_tup is None:
#             id_tup=set()
#         id_tup.add(tup)
#         id2tuples[idd]=id_tup
# 
#         count+=1
#     read5M.close()
#     print 'load_id2tuples finished' 
#     return id2tuples 
# def load_groundtruth_tuple(infile):
#     readfile=codecs.open(infile, 'r', 'utf-8')
#     tuple_list=[]
#     for line in readfile:
#         parts=line.strip().split('\t')
#         idd='m.'+parts[0][last_slash_pos(parts[0])+1:]
#         relation=parts[1][last_slash_pos(parts[1])+1:]  
#         tuple_list.append((idd,relation))
#     readfile.close()
#     print 'load_groundtruth_tuple finished'
#     return tuple_list      
# def load_fix_Q_mention(fil):
#     men_Q=[]
#     readfile=codecs.open(fil, 'r', 'utf-8')
#     for line in readfile:
#         parts=line.strip().split('\t')
#         Q=parts[0]
#         men=parts[1]
#         men_Q.append((men, Q))
#     readfile.close()
#     print 'load_fix_Q_mention finished'
#     return men_Q
# def EntityLinkingResult_into_TrainModelInput_TestValid_FixMention():
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     id2name, id2des=load_id2names_id2des()
#     id2tuples=load_id2tuples()
# #     name=id2name.get('m.03g_jj2')
# #     des=id2des.get('m.03g_jj2')
# #     tuples=id2tuples.get('m.03g_jj2')
# #     print name, des, tuples
# #     exit(0)
# #     print 'id2tuples.get:', id2tuples.get('m.0c1rnhp')
# #     exit(0)
#  
#     test_valid=['annotated_fb_data_test.entitylinking.top20_succSet.txt', 'annotated_fb_data_valid.entitylinking.top20_succSet.txt']
#     raw_test_valid=['annotated_fb_data_test_succSet.txt', 'annotated_fb_data_valid_succSet.txt']  
#     Q_mention_files=['annotated_fb_data_test_Q_fixMention_succSet.txt', 'annotated_fb_data_valid_Q_fixMention_succSet.txt'] 
#     for i in range(2):
#         nega_size=0
#         readfile=codecs.open(path+test_valid[i], 'r', 'utf-8')
#         ground_tuple_list=load_groundtruth_tuple(path+raw_test_valid[i])
#         fix_men_Q=load_fix_Q_mention(path+Q_mention_files[i])
#         if len(ground_tuple_list)!=len(fix_men_Q):
#             print 'len(ground_tuple_list)!=len(fix_men_Q):', len(ground_tuple_list), len(fix_men_Q)
#             exit(0)
# #         print fix_men_Q[-1]
# #         exit(0)
#         if i==0:
#             writefile=codecs.open(path+'annotated_fb_data_test.entitylinking.top20_succSet_mixMenQ_asInput.txt', 'w', 'utf-8')  
#         else:
#             writefile=codecs.open(path+'annotated_fb_data_valid.entitylinking.top20_succSet_mixMenQ_asInput.txt', 'w', 'utf-8')
#         count=0
#         for line in readfile:
#             neg_size_line=0
#             parts=line.strip().split()
# #             print 'len(parts):', len(parts)
#             entity_parts=parts[:20]
#             question=parts[20:]
#             if parts[20].find('==')>=0:
#                 print 'format error'
#                 exit(0)
#             ground_tuple=ground_tuple_list[count]
# #             nega_tuples=set()
#             tuple_write=[]
#             name_write=[]
#             des_write=[]
#             men_Q_write=[]
# #             if count==1347:
# #                 print entity_parts
# #                 exit(0)
# #             print id2tuples.get('m.03g_jj2'), count
#             for p in range(20):
#                 part=entity_parts[p]
# #             for part in parts[:-1]:
#                 tokens=part.strip().split('==')
#                 mid=tokens[0]
# #                 print 'mid:', mid
#                 s1=tokens[1]
#                 s2=tokens[2]
#                 s3=tokens[3]
#                 s4=tokens[4]
#                 mid_related_tuples=id2tuples.get(mid, set()).copy()
# #                 neg_size_line+=len(mid_related_tuples)
#                 mid_name_str=id2name.get(mid)
#                 mid_name=mid_name_str.split()
#                 mid_des=id2des.get(mid)
# #                 if mid=='m.03g_jj2' and count==1347:
# #                     print mid_related_tuples, mid_name_str, mid_des, p
#                 if len(mid_related_tuples)==0:
#                     if p==0:
#                         tuple_write.append('=='.join(ground_tuple)+'=='+'=='.join([s1,s2,s3,s4]))
#                         name_write.append(mid_name_str)
#                         des_write.append(mid_des)
#                         fix_men=fix_men_Q[count][0]
#                         fix_Q=fix_men_Q[count][1]
#                         dy_men_Q=list(mention_detection_given_questionAndEntity(question, mid_name))
#                         if len(set(fix_men.split())&set(dy_men_Q[0].split()))>0:
#                             men_Q_write.append('=='.join(dy_men_Q))      
#                         else:        
#                             men_Q_write.append('=='.join([fix_men, fix_Q]))       
#                     continue
#                 else:
#                     if p==0:
#                         tuple_write.append('=='.join(ground_tuple)+'=='+'=='.join([s1,s2,s3,s4]))
#                         name_write.append(mid_name_str)
#                         des_write.append(mid_des)
#                         fix_men=fix_men_Q[count][0]
#                         fix_Q=fix_men_Q[count][1]
#                         dy_men_Q=list(mention_detection_given_questionAndEntity(question, mid_name))
#                         if len(set(fix_men.split())&set(dy_men_Q[0].split()))>0:
#                             men_Q_write.append('=='.join(dy_men_Q))      
#                         else:        
#                             men_Q_write.append('=='.join([fix_men, fix_Q])) 
#                         if ground_tuple in mid_related_tuples:
#                             mid_related_tuples.remove(ground_tuple)
#                             
#                 if mid_name_str not in  string.punctuation :
#                     for related_tup in mid_related_tuples:
#                         tuple_write.append('=='.join(related_tup)+'=='+'=='.join([s1,s2,s3,s4]))
#                         name_write.append(mid_name_str)
#                         des_write.append(mid_des)
#                         fix_men=fix_men_Q[count][0]
#                         fix_Q=fix_men_Q[count][1]
#                         dy_men_Q=list(mention_detection_given_questionAndEntity(question, mid_name))
#                         if len(set(fix_men.split())&set(dy_men_Q[0].split()))>0:
#                             men_Q_write.append('=='.join(dy_men_Q))      
#                         else:        
#                             men_Q_write.append('=='.join([fix_men, fix_Q])) 
#             
#             neg_size_line=len(tuple_write)
#             nega_size+=neg_size_line
#             #shuffle
# #             if len(tuple_write)!=len(des_write) or  len(tuple_write)!=len(name_write) or len(tuple_write)!=len(men_Q_write) or len(tuple_write)!=neg_size_line:
# #                 print 'tuple_write, des_write, men_Q_write, size not equal'
# #                 print 'len(tuple_write):', len(tuple_write)
# #                 print 'len(name_write):', len(name_write)
# #                 print 'len(des_write):', len(des_write)
# #                 print 'len(men_Q_write):', len(men_Q_write)
# #                 print 'neg_size_line:', neg_size_line
# #                 exit(0)
# #             print 'neg_size_line:', neg_size_line
#             index_list=range(1, neg_size_line)
#             shuffle(index_list)
# #             print 'index_list:', index_list
#             indices=[0]+index_list
#             writefile.write(str(neg_size_line)+'\t')
#             writefile.write('\t'.join([tuple_write[ind] for ind in indices])+'\t')
#             writefile.write('\t'.join([name_write[ind] for ind in indices])+'\t')
#             writefile.write('\t'.join([des_write[ind] for ind in indices])+'\t')
#             writefile.write('\t'.join([men_Q_write[ind] for ind in indices])+'\n')
#             count+=1
#         readfile.close()
#         writefile.close()
#         print i, 'finished'  
# def EntityLinkingResult_into_TrainModelInput_TestValid():
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     id2name, id2des=load_id2names_id2des()
#     id2tuples=load_id2tuples()
# #     name=id2name.get('m.03g_jj2')
# #     des=id2des.get('m.03g_jj2')
# #     tuples=id2tuples.get('m.03g_jj2')
# #     print name, des, tuples
# #     exit(0)
# #     print 'id2tuples.get:', id2tuples.get('m.0c1rnhp')
# #     exit(0)
#  
#     test_valid=['annotated_fb_data_test.entitylinking.top20_succSet.txt', 'annotated_fb_data_valid.entitylinking.top20_succSet.txt']
#     raw_test_valid=['annotated_fb_data_test_succSet.txt', 'annotated_fb_data_valid_succSet.txt']   
#     for i in range(2):
#         nega_size=0
#         readfile=codecs.open(path+test_valid[i], 'r', 'utf-8')
#         ground_tuple_list=load_groundtruth_tuple(path+raw_test_valid[i])
#         if i==0:
#             writefile=codecs.open(path+'annotated_fb_data_test.entitylinking.top20_succSet_asInput.txt', 'w', 'utf-8')  
#         else:
#             writefile=codecs.open(path+'annotated_fb_data_valid.entitylinking.top20_succSet_asInput.txt', 'w', 'utf-8')
#         count=0
#         for line in readfile:
#             neg_size_line=0
#             parts=line.strip().split()
# #             print 'len(parts):', len(parts)
#             entity_parts=parts[:20]
#             question=parts[20:]
#             if parts[20].find('==')>=0:
#                 print 'format error'
#                 exit(0)
#             ground_tuple=ground_tuple_list[count]
# #             nega_tuples=set()
#             tuple_write=[]
#             name_write=[]
#             des_write=[]
#             men_Q_write=[]
# #             if count==1347:
# #                 print entity_parts
# #                 exit(0)
# #             print id2tuples.get('m.03g_jj2'), count
#             for p in range(20):
#                 part=entity_parts[p]
# #             for part in parts[:-1]:
#                 tokens=part.strip().split('==')
#                 mid=tokens[0]
# #                 print 'mid:', mid
#                 s1=tokens[1]
#                 s2=tokens[2]
#                 s3=tokens[3]
#                 s4=tokens[4]
#                 mid_related_tuples=id2tuples.get(mid, set()).copy()
# #                 neg_size_line+=len(mid_related_tuples)
#                 mid_name_str=id2name.get(mid)
#                 mid_name=mid_name_str.split()
#                 mid_des=id2des.get(mid)
# #                 if mid=='m.03g_jj2' and count==1347:
# #                     print mid_related_tuples, mid_name_str, mid_des, p
#                 if len(mid_related_tuples)==0:
#                     if p==0:
#                         tuple_write.append('=='.join(ground_tuple)+'=='+'=='.join([s1,s2,s3,s4]))
#                         name_write.append(mid_name_str)
#                         des_write.append(mid_des)
#                         men_Q_write.append('=='.join(list(mention_detection_given_questionAndEntity(question, mid_name))))                   
#                     continue
#                 else:
#                     if p==0:
#                         tuple_write.append('=='.join(ground_tuple)+'=='+'=='.join([s1,s2,s3,s4]))
#                         name_write.append(mid_name_str)
#                         des_write.append(mid_des)
#                         men_Q_write.append('=='.join(list(mention_detection_given_questionAndEntity(question, mid_name))))
#                         if ground_tuple in mid_related_tuples:
#                             mid_related_tuples.remove(ground_tuple)
#                             
#                 if mid_name_str not in  string.punctuation :
#                     for related_tup in mid_related_tuples:
#                         tuple_write.append('=='.join(related_tup)+'=='+'=='.join([s1,s2,s3,s4]))
#                         name_write.append(mid_name_str)
#                         des_write.append(mid_des)
#                         men_Q_write.append('=='.join(list(mention_detection_given_questionAndEntity(question, mid_name))))
#             
#             neg_size_line=len(tuple_write)
#             nega_size+=neg_size_line
#             #shuffle
# #             if len(tuple_write)!=len(des_write) or  len(tuple_write)!=len(name_write) or len(tuple_write)!=len(men_Q_write) or len(tuple_write)!=neg_size_line:
# #                 print 'tuple_write, des_write, men_Q_write, size not equal'
# #                 print 'len(tuple_write):', len(tuple_write)
# #                 print 'len(name_write):', len(name_write)
# #                 print 'len(des_write):', len(des_write)
# #                 print 'len(men_Q_write):', len(men_Q_write)
# #                 print 'neg_size_line:', neg_size_line
# #                 exit(0)
# #             print 'neg_size_line:', neg_size_line
#             index_list=range(1, neg_size_line)
#             shuffle(index_list)
# #             print 'index_list:', index_list
#             indices=[0]+index_list
#             writefile.write(str(neg_size_line)+'\t')
#             writefile.write('\t'.join([tuple_write[ind] for ind in indices])+'\t')
#             writefile.write('\t'.join([name_write[ind] for ind in indices])+'\t')
#             writefile.write('\t'.join([des_write[ind] for ind in indices])+'\t')
#             writefile.write('\t'.join([men_Q_write[ind] for ind in indices])+'\n')
#             count+=1
#         readfile.close()
#         writefile.close()
#         print i, 'finished'
#                 
# 
# def EntityLinkingResult_into_TrainModelInput_Train():
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     id2name, id2des=load_id2names_id2des()
# #     print 'Name of m.03qqv6f:', id2name.get('m.03qqv6f')
#     id2tuples=load_id2tuples()
#     max_triples=100
#     train='annotated_fb_data_train.entitylinking.top20_remove_error.txt'
#     raw_train='annotated_fb_data_train.txt'  
# 
#     readfile=codecs.open(path+train, 'r', 'utf-8')
#     ground_tuple_list=load_groundtruth_tuple(path+raw_train)
#     ground_tuple_list.pop(31858)
#     writefile=codecs.open(path+'annotated_fb_data_train.entitylinking.top20_succSet_asInput.txt', 'w', 'utf-8')  
# 
#     count=0
#     for line in readfile:
#         
#         neg_size_line=0
#         parts=line.strip().split()
# #             print 'len(parts):', len(parts)
#         entity_parts=parts[:20]
#         question=parts[20:]
#         if parts[20].find('==')>=0:
#             print 'format error'
#             exit(0)
#         ground_tuple=ground_tuple_list[count]
# #         if ' '.join(question)=='who is the artist behind viaduct':
# #             print 'line:', line
# 
# #             nega_tuples=set()
#         tuple_write=[]
#         name_write=[]
#         des_write=[]
#         men_Q_write=[]
#         for p in range(20):
#             part=entity_parts[p]
# #             for part in parts[:-1]:
#             tokens=part.strip().split('==')
#             mid=tokens[0]
# #             if ' '.join(question)=='who is the artist behind viaduct':
# #                 print 'p:', p
# #                 print 'tuple:', part
#             s1=tokens[1]
#             s2=tokens[2]
#             s3=tokens[3]
#             s4=tokens[4]
#             mid_related_tuples=id2tuples.get(mid, set()).copy()
#             mid_name_str=id2name.get(mid, 'unknown')
#             mid_name=mid_name_str.split()
#             mid_des=id2des.get(mid, 'unknown')
# #                 print mid, mid_related_tuples, len(mid_related_tuples)
#             if len(mid_related_tuples)==0:
#                 if p==0:
#                     tuple_write.append('=='.join(ground_tuple)+'=='+'=='.join([s1,s2,s3,s4]))
#                     name_write.append(mid_name_str)
#                     des_write.append(mid_des)
#                     men_Q_write.append('=='.join(list(mention_detection_given_questionAndEntity(question, mid_name))))
#                 continue
# #                 neg_size_line+=len(mid_related_tuples)
# 
#             else:            
#                 if p==0:
#                     tuple_write.append('=='.join(ground_tuple)+'=='+'=='.join([s1,s2,s3,s4]))
#                     name_write.append(mid_name_str)
#                     des_write.append(mid_des)
#                     men_Q_write.append('=='.join(list(mention_detection_given_questionAndEntity(question, mid_name))))
#                     if ground_tuple in mid_related_tuples:
#                         mid_related_tuples.remove(ground_tuple)
#             if mid_name_str not in  string.punctuation :
#                 for related_tup in mid_related_tuples:
#                     tuple_write.append('=='.join(related_tup)+'=='+'=='.join([s1,s2,s3,s4]))
#                     name_write.append(mid_name_str)
#                     des_write.append(mid_des)
#                     men_Q_write.append('=='.join(list(mention_detection_given_questionAndEntity(question, mid_name))))
#         
#         neg_size_line=len(tuple_write)
#         if neg_size_line==1:
#             count+=1
#             continue
#         index_list=range(1, neg_size_line)
#         if neg_size_line<max_triples:
#             times=(max_triples-1)/(neg_size_line-1)
#             remain=(max_triples-1)%(neg_size_line-1)
#             sampled_list=sample(set(index_list), remain)
#             index_list=index_list*times+sampled_list
#         elif neg_size_line>max_triples:
# #             index_list=index_list[:max_triples-1]
#             index_list=sample(set(index_list), max_triples-1)
# 
#         shuffle(index_list)
# #             print 'index_list:', index_list
#         indices=[0]+index_list
#         if len(indices)!=max_triples:
#             print 'len(indices)!=max_triples'
#             exit(0)
#         writefile.write(str(max_triples)+'\t')
# #         if ' '.join(question)=='who is the artist behind viaduct':
# #             print 'ground_tuple:', ground_tuple
# #             print 'name_write[0]:', name_write
# #             print 'des_write[0]:', des_write[0]
# #             exit(0)
#         writefile.write('\t'.join([tuple_write[ind] for ind in indices])+'\t')
#         writefile.write('\t'.join([name_write[ind] for ind in indices])+'\t')
#         writefile.write('\t'.join([des_write[ind] for ind in indices])+'\t')
#         writefile.write('\t'.join([men_Q_write[ind] for ind in indices])+'\n')
# 
#         count+=1
#     readfile.close()
#     writefile.close()
#     print 'finished'
# def EntityLinkingResult_into_TrainModelInput_Train_FixMention():
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     id2name, id2des=load_id2names_id2des()
# #     print 'Name of m.03qqv6f:', id2name.get('m.03qqv6f')
#     id2tuples=load_id2tuples()
#     max_triples=100
#     train='annotated_fb_data_train.entitylinking.top20_remove_error.txt'
#     raw_train='annotated_fb_data_train.txt'  
#     men_Q_train='annotated_fb_data_train.questions_fixedMentions_goldEntity_remove_error.txt'
#     readfile=codecs.open(path+train, 'r', 'utf-8')
#     ground_tuple_list=load_groundtruth_tuple(path+raw_train)
#     ground_tuple_list.pop(31858)
#     fix_men_Q=load_fix_Q_mention(path+men_Q_train)
#     if len(ground_tuple_list)!=len(fix_men_Q):
#         print 'len(ground_tuple_list)!=len(fix_men_Q):', len(ground_tuple_list), len(fix_men_Q)
#         exit(0)
#     writefile=codecs.open(path+'annotated_fb_data_train.entitylinking.top20_succSet_mixMenQ_asInput.txt', 'w', 'utf-8')  
# 
#     count=0
#     for line in readfile:
#         
#         neg_size_line=0
#         parts=line.strip().split()
# #             print 'len(parts):', len(parts)
#         entity_parts=parts[:20]
#         question=parts[20:]
#         if parts[20].find('==')>=0:
#             print 'format error'
#             exit(0)
#         ground_tuple=ground_tuple_list[count]
# #         if ' '.join(question)=='who is the artist behind viaduct':
# #             print 'line:', line
# 
# #             nega_tuples=set()
#         tuple_write=[]
#         name_write=[]
#         des_write=[]
#         men_Q_write=[]
#         for p in range(20):
#             part=entity_parts[p]
# #             for part in parts[:-1]:
#             tokens=part.strip().split('==')
#             mid=tokens[0]
# #             if ' '.join(question)=='who is the artist behind viaduct':
# #                 print 'p:', p
# #                 print 'tuple:', part
#             s1=tokens[1]
#             s2=tokens[2]
#             s3=tokens[3]
#             s4=tokens[4]
#             mid_related_tuples=id2tuples.get(mid, set()).copy()
#             mid_name_str=id2name.get(mid, 'unknown')
#             mid_name=mid_name_str.split()
#             mid_des=id2des.get(mid, 'unknown')
# #                 print mid, mid_related_tuples, len(mid_related_tuples)
#             if len(mid_related_tuples)==0:
#                 if p==0:
#                     tuple_write.append('=='.join(ground_tuple)+'=='+'=='.join([s1,s2,s3,s4]))
#                     name_write.append(mid_name_str)
#                     des_write.append(mid_des)
#                     fix_men=fix_men_Q[count][0]
#                     fix_Q=fix_men_Q[count][1]
#                     dy_men_Q=list(mention_detection_given_questionAndEntity(question, mid_name))
#                     if len(set(fix_men.split())&set(dy_men_Q[0].split()))>0:
#                         men_Q_write.append('=='.join(dy_men_Q))      
#                     else:        
#                         men_Q_write.append('=='.join([fix_men, fix_Q]))
#                 continue
# #                 neg_size_line+=len(mid_related_tuples)
# 
#             else:            
#                 if p==0:
#                     tuple_write.append('=='.join(ground_tuple)+'=='+'=='.join([s1,s2,s3,s4]))
#                     name_write.append(mid_name_str)
#                     des_write.append(mid_des)
#                     fix_men=fix_men_Q[count][0]
#                     fix_Q=fix_men_Q[count][1]
#                     dy_men_Q=list(mention_detection_given_questionAndEntity(question, mid_name))
#                     if len(set(fix_men.split())&set(dy_men_Q[0].split()))>0:
#                         men_Q_write.append('=='.join(dy_men_Q))      
#                     else:        
#                         men_Q_write.append('=='.join([fix_men, fix_Q]))
#                     if ground_tuple in mid_related_tuples:
#                         mid_related_tuples.remove(ground_tuple)
#             if mid_name_str not in  string.punctuation :
#                 for related_tup in mid_related_tuples:
#                     tuple_write.append('=='.join(related_tup)+'=='+'=='.join([s1,s2,s3,s4]))
#                     name_write.append(mid_name_str)
#                     des_write.append(mid_des)
#                     fix_men=fix_men_Q[count][0]
#                     fix_Q=fix_men_Q[count][1]
#                     dy_men_Q=list(mention_detection_given_questionAndEntity(question, mid_name))
#                     if len(set(fix_men.split())&set(dy_men_Q[0].split()))>0:
#                         men_Q_write.append('=='.join(dy_men_Q))      
#                     else:        
#                         men_Q_write.append('=='.join([fix_men, fix_Q]))
#         
#         neg_size_line=len(tuple_write)
#         if neg_size_line==1:
#             count+=1
#             continue
#         index_list=range(1, neg_size_line)
#         if neg_size_line<max_triples:
#             times=(max_triples-1)/(neg_size_line-1)
#             remain=(max_triples-1)%(neg_size_line-1)
#             sampled_list=sample(set(index_list), remain)
#             index_list=index_list*times+sampled_list
#         elif neg_size_line>max_triples:
# #             index_list=index_list[:max_triples-1]
#             index_list=sample(set(index_list), max_triples-1)
# 
#         shuffle(index_list)
# #             print 'index_list:', index_list
#         indices=[0]+index_list
#         if len(indices)!=max_triples:
#             print 'len(indices)!=max_triples'
#             exit(0)
#         writefile.write(str(max_triples)+'\t')
# #         if ' '.join(question)=='who is the artist behind viaduct':
# #             print 'ground_tuple:', ground_tuple
# #             print 'name_write[0]:', name_write
# #             print 'des_write[0]:', des_write[0]
# #             exit(0)
#         writefile.write('\t'.join([tuple_write[ind] for ind in indices])+'\t')
#         writefile.write('\t'.join([name_write[ind] for ind in indices])+'\t')
#         writefile.write('\t'.join([des_write[ind] for ind in indices])+'\t')
#         writefile.write('\t'.join([men_Q_write[ind] for ind in indices])+'\n')
# 
#         count+=1
#     readfile.close()
#     writefile.close()
#     print 'finished'                
# def mention_detection_given_questionAndEntity_characterLevel(a, b):
# #     print 'a:', a
# #     print 'b:', b
#     len_a=len(a)
#     len_b=len(b)
#     a_label=[0]*len_a
#     b_label=[0]*len_b
#     table=[[0]*(len_b+1) for _ in xrange(len_a+1)]
#     l=0
#     for i, ca in enumerate(a,1):
#         for j, cb in enumerate(b,1):
#             if ca==cb:
#                 table[i][j]=table[i-1][j-1]+1
#                 if table[i][j]>=l:
#                     l=table[i][j]
#                     a_label[i-1]=1
#                     b_label[j-1]=1
#     
# #     print 'l:', l
# #     print 'a_label:', a_label
# #     print 'b_label:', b_label
#     if l==0:
#         return ''.join(b), ''.join(a)
#     
#     a_last_1_posi=len_a-1
#     while a_label[a_last_1_posi]!=1:
#         a_last_1_posi-=1
#     a_first_1_posi=a_last_1_posi-l+1
#     
#     
#     while a_last_1_posi+1<len_a:
#         if a[a_last_1_posi+1]!=' ': 
#             a_last_1_posi+=1
#         else:
#             break
#     while a_first_1_posi-1>=0:
#         if a[a_first_1_posi-1]!=' ': 
#             a_first_1_posi-=1
#         else:
#             break
# #     while a[a_first_1_posi]!=' ':
# #         if a_first_1_posi>0:
# #             a_first_1_posi-=1
# #         else:
# #             break
#     
#     
#     
# #     b_last_1_posi=len_b-1
# #     while b_label[b_last_1_posi]!=1:
# #         b_last_1_posi-=1
# #     b_first_1_posi=b_last_1_posi-l+1    
# #     print a_label, b_label
# 
# 
# #     print a_last_1_posi, (len_b-b_last_1_posi)
# #     a_last_1_posi+=(len_b-b_last_1_posi-1)
# #     print a_last_1_posi
#     mention=''.join(a[a_first_1_posi:a_last_1_posi+1]).strip()
#     question_minus=''.join(a[:a_first_1_posi]+[' <e> ']+a[a_last_1_posi+1:]).strip()
#     
#     return mention, question_minus           
#             
# def mention_detection_given_questionAndEntity(a, b):
#     len_a=len(a)
#     len_b=len(b)
#     a_label=[0]*len_a
#     b_label=[0]*len_b
#     table=[[0]*(len_b+1) for _ in xrange(len_a+1)]
#     l=0
#     for i, ca in enumerate(a,1):
#         for j, cb in enumerate(b,1):
#             if ca==cb:
#                 table[i][j]=table[i-1][j-1]+1
#                 if table[i][j]>l:
#                     l=table[i][j]
#                     a_label[i-1]=1
#                     b_label[j-1]=1
#     
#     if l==0:
# #         print 'enter char level'
#         men, q_=mention_detection_given_questionAndEntity_characterLevel(list(' '.join(a)), list(' '.join(b)))
#         return men, q_
#     
#     a_last_1_posi=len_a-1
#     while a_label[a_last_1_posi]!=1:
#         a_last_1_posi-=1
#     a_first_1_posi=a_last_1_posi-l+1
#     
#     b_last_1_posi=len_b-1
#     while b_label[b_last_1_posi]!=1:
#         b_last_1_posi-=1
#     b_first_1_posi=b_last_1_posi-l+1    
# #     print a_label, b_label
#     a_first_1_posi=max(0, a_first_1_posi-b_first_1_posi)
#     a_last_1_posi+=(len_b-b_last_1_posi-1)
#     a_first_1_posi=max(0, a_first_1_posi)
#     mention=' '.join(a[a_first_1_posi:a_last_1_posi+1])
#     question_minus=' '.join(a[:a_first_1_posi]+['<e>']+a[a_last_1_posi+1:])
#     
#     return mention, question_minus
#                 
#             
# def remove_error():
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     id2name, id2des=load_id2names_id2des()
# 
#     raw_train='annotated_fb_data_train.txt'  
#     ground_tuple_list=load_groundtruth_tuple(path+raw_train)
#     ground_tuple_list.pop(31858)
#     
#     line_co=0
#     readfile=codecs.open(path+'annotated_fb_data_train.entitylinking.top20.txt' , 'r', 'utf-8')         
#     writefile=codecs.open(path+'annotated_fb_data_train.entitylinking.top20_remove_error.txt' , 'w', 'utf-8')  
#     for line in readfile:
#         if line_co<31858:
#             writefile.write(line.strip()+'\n')
#         else:
#             parts=line.strip().split()
#             ground_tuple=ground_tuple_list[line_co]
#             question_list=parts[20:]
#             mid=ground_tuple[0]
#             name=id2name.get(mid, 'unknown')
# #             if line_co>30000:
# #                 print mid, name
# 
# #             if line_co>30000:
# #                 print question_list, name
#             s1, s2, s3, s4=lcsubstring_length(question_list, name.split())
#             new_part=mid+'=='+str(s1)+'=='+str(s2)+'=='+str(s3)+'=='+str(s4)
#             new_parts=[new_part]+parts[1:]
#             writefile.write(' '.join(new_parts)+'\n')
#         line_co+=1
#         if line_co%10000==0:
#             print line_co
#     readfile.close()
#     writefile.close()
#     print 'remove error over'
# 
# def load_link_label_and_goldIDs():
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     row2label=[]
#     row2id=[]
#     readfile=codecs.open(path+'annotated_fb_data_test.entitylinking.top20.txt', 'r', 'utf-8')        
#     for line in readfile:
#         parts=line.strip().split()
#         row2label.append(parts[0])   
#         row2id.append(parts[1].split('==')[0])
#     readfile.close()
#     print 'load_link_label_and_goldIDs over'
#     return row2label, row2id
# def check_groundtruth_test():
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
# 
#     gold_id_list=load_gold_head_ids(path+'annotated_fb_data_test.txt')    
#     link_label, link_ids=load_link_label_and_goldIDs()
#     length=len(gold_id_list)
#     if length!=len(link_label) or length!=len(link_ids):
#         print 'size not equal'
#         exit(0)
#     
#     for i in range(length):
#         if link_label[i]=='1':
#             if gold_id_list[i]!=link_ids[i]:
#                 print 'i:', i, 'id not equal:', gold_id_list[i], link_ids[i]
#     print 'check over'
# 
# def position_of_OneSequence_in_binary_list(biList):
#     length=len(biList)
#     start=-1
#     len_t=0 #len of 1 sequence
#     position_set=set()
#     for i in range(length):
#         if biList[i]==0:
#             if start==-1:
#                 continue
#             else:
#                 position_set.add((start, start+len_t))
#                 start=-1
#                 len_t=0
#         else:
#             if start==-1:
#                 start=i
#             len_t+=1
#             if i==length-1:
#                 position_set.add((start, start+len_t))
#     return position_set
# 
#     
# def select_best_nn_position(start_end_pair_set, sent_len):
#     pair2score={}
#     for pair in  start_end_pair_set:
#         start=pair[0]
#         end=pair[1]
#         score=(end-start)*4.5/sent_len+(end-1)*1.0/sent_len   
#         pair2score[pair]=score
#     sorted_map=sorted(pair2score.items(), key=operator.itemgetter(1), reverse=True)
#     return sorted_map[0][0]
# def detect_mention_indicators_by_postags(sent_len, pos_list, NN_labels, copy_next_labels):
#     #first round
#     indicator_list=[0]*sent_len
#     nn_exist=False
#     for i in range(sent_len):
#         if pos_list[i] in NN_labels:
#             indicator_list[i]=1
#             nn_exist=True
#     #second round
#     for i in range(sent_len):
#         if pos_list[i] in copy_next_labels:
#             if i+1<sent_len:
#                 if indicator_list[i+1]==1:
#                     indicator_list[i]=1 
#                     nn_exist=True     
#     return    nn_exist,  indicator_list
# def detect_mention(token_POS_str):
# #     print 'token_POS_str:', token_POS_str
#     NN_labels={'NN', 'NNS', 'NNP', 'NNPS', 'FW'}
#     copy_next_labels={'JJ', 'JJR', 'JJS', 'CD'}
#     
#     secondStage_labels={'PRP', 'JJ', 'CD', 'JJR'}
#     secondStage_copy_next_labels={'PRP', 'VBP'}
#     
#     thirdStage_labels={'RB', 'VB', 'VBN', 'VBG', 'VBD', 'VBP', 'IN'}
#     thirdStage_copy_next_labels={'VBN'}
#     
#     fourStage_labels={'WP'}
#     fourStage_copy_next_labels=set()
#     parts=token_POS_str.split()
#     sent_len=len(parts)
#     token_list=[]
#     pos_list=[]
#     for part in parts:
#         tokens=part.split('_')
#         token_list.append(tokens[0].lower())
#         if len(tokens)==2:
#             pos_list.append(tokens[1])
#         else:
#             pos_list.append('UNK')
#     nn_exist, indicator_list=detect_mention_indicators_by_postags(sent_len, pos_list, NN_labels, copy_next_labels)
#     if nn_exist is False:
#         nn_exist, indicator_list=detect_mention_indicators_by_postags(sent_len, pos_list, secondStage_labels, secondStage_copy_next_labels)
#     if nn_exist is False:
#         nn_exist, indicator_list=detect_mention_indicators_by_postags(sent_len, pos_list, thirdStage_labels, thirdStage_copy_next_labels)
#     if nn_exist is False:
#         nn_exist, indicator_list=detect_mention_indicators_by_postags(sent_len, pos_list, fourStage_labels, fourStage_copy_next_labels)
# #     #first round
# #     indicator_list=[0]*sent_len
# #     nn_exist=False
# #     for i in range(sent_len):
# #         if pos_list[i] in NN_labels:
# #             indicator_list[i]=1
# #             nn_exist=True
# #     #second round
# #     for i in range(sent_len):
# #         if pos_list[i] in copy_next_labels:
# #             if i+1<sent_len:
# #                 if indicator_list[i+1]==1:
# #                     indicator_list[i]=1 
# #                     nn_exist=True  
# 
#    
#     if nn_exist:
#         start_end_pair_set=position_of_OneSequence_in_binary_list(indicator_list)
#         best_pair=select_best_nn_position(start_end_pair_set, sent_len)
#         mention=' '.join(token_list[best_pair[0]:best_pair[1]])
#         question=(' '.join(token_list[:best_pair[0]])+' <e> '+' '.join(token_list[best_pair[1]:])).strip()
#         return question, mention
#     else:
#         print 'find no valid mention from:', token_POS_str
#         exit(0)
#         
#         
#     
#     
#     
#         
# def detect_fixed_mentions():
#     #load is2name
#     path='/mounts/data/proj/wenpeng/Dataset/freebase/SimpleQuestions_v2/'
#     id2name, id2des=load_id2names_id2des()
#     rfiles=['annotated_fb_data_test.questions_combinedPOS.txt', 'annotated_fb_data_valid.questions_combinedPOS.txt', 'annotated_fb_data_train.questions_combinedPOS.txt']       
#     wfiles=['annotated_fb_data_test.questions_fixedMentions_goldEntity.txt', 'annotated_fb_data_valid.questions_fixedMentions_goldEntity.txt', 'annotated_fb_data_train.questions_fixedMentions_goldEntity.txt']   
#     groundfiles=['annotated_fb_data_test.txt', 'annotated_fb_data_valid.txt', 'annotated_fb_data_train.txt']
#         
#     for i in range(3):
#         all_size=0
#         corr_size=0
#         gold_id_list=load_gold_head_ids(path+groundfiles[i])
#         readfile=codecs.open(path+rfiles[i], 'r', 'utf-8')
#         writefile=codecs.open(path+wfiles[i], 'w', 'utf-8')
#         
#         for line in readfile:
#             question, mention=detect_mention(line.strip())
#             gold_entity=id2name.get(gold_id_list[all_size], 'UNK')
#             writefile.write(question+'\t'+mention+'\t'+gold_entity+'\n')
#             if len(set(mention.split())& set(gold_entity.split()))>0:
#                 corr_size+=1
# #             else:
# #                 print line.strip(), mention, gold_entity
#             all_size+=1
#         readfile.close()
#         writefile.close()
#         print i, 'finished, corr rato:', corr_size*1.0/all_size
# #         exit(0)


def  from_MoFormat_to_WenpengFormat():
    #first load id2relation
    path='/home/wyin/Datasets/SimpleQuestions_v2/relation_classification/'
    readfile=codecs.open(path+'relations.with_label.txt', 'r', 'utf-8')
    id2rel={}
    co=0
    for line in readfile:
        if co>0:
            parts=line.strip().split()
            id=int(parts[0])
            rel=' '.join(parts[2:])
            id2rel[id]=rel
        co+=1
    readfile.close()
    
    #load train and test
    files=['train.replace_ne.withpool', 'test.replace_ne.withpool', 'valid.replace_ne.withpool']
    for i in range(1,3):
        readfile=codecs.open(path+files[i], 'r', 'utf-8')
        writefile=codecs.open(path+files[i]+'wenpengFormat.txt', 'w', 'utf-8')
        co=0
        for line in readfile:
            if co>0:
                parts=line.strip().split('\t')
                if parts[1]=='noGenativeAnswer':
                    co+=1
                    continue
                else:
                    gold_id=int(parts[0])
                    neg_ids=set(map(int, parts[1].strip().split()))-set([gold_id])
                    if len(neg_ids)==0:
                        co+=1
                        continue
                    else:
                        writefile.write(id2rel.get(gold_id)+'\t')
                        writefile.write('\t'.join([id2rel.get(int(neg_id)) for neg_id in neg_ids])+'\t'+parts[2]+'\n')
            co+=1
        writefile.close()
        readfile.close()
        print i, 'finished'

   
if __name__ == '__main__':
    from_MoFormat_to_WenpengFormat()