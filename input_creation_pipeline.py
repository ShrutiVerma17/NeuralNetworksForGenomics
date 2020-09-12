#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 19:59:11 2020

@author: shrutiverma
"""
from Bio import SeqIO
import numpy as np
import argparse

def parse_args():
    parser=argparse.ArgumentParser(description="creating files")
    parser.add_argument("--dir")
    parser.add_argument("--length")
    return parser.parse_args()

def main():
    args=parse_args()
    my_dir = args.dir
    length = args.length
    # open each of the 10 chromosome files
    # loop through them, grabbing the first 300 of their sequences (random) and the last 300 and adding it to two separate files, one called "first_300_all" and one called "second_300_all"
    # count the number of introns and exons in each, and balance into final files
    
    mega_file = open("mega_imbalanced_file", "w+")
    sequence_length = length
    
    introns = 0
    cds_exons = 0
    five_prime_exons = 0
    three_prime_exons = 0
    
    #  This line is for when you're trying to create a balanced input file
    #  or (file == "introns.fa" and introns > NUMBER)
    
    for i in range (1, 5):
      fileDir = my_dir + str(i)
      files_to_parse = ["cds_exons.fa", "utr_3_prime.fa", "utr_5_prime.fa", "introns.fa"]
      for file in files_to_parse:
        fileName = fileDir + "/" + file
        for record in SeqIO.parse(fileName, "fasta"):
          myseq = record.seq
          if (str(myseq).count('N') > 0 or str(myseq).count('n') > 0 or len(myseq) <= sequence_length or (file == "introns.fa" and len(myseq) <= sequence_length + 200)):
            pass
          else:
            if (file == "cds_exons.fa"):
              cds_exons += 1
              sequence = str(myseq).upper()
              sequence = sequence[0:sequence_length]
              if (len(sequence) != sequence_length):
                print("ERROR")
                break
              mega_file.write(sequence + "\n")
            elif (file == "utr_3_prime.fa"):
              three_prime_exons += 1
              sequence = str(myseq).lower()
              sequence = sequence[0].upper() + sequence[1:]
              sequence = sequence[0:sequence_length]
              if (len(sequence) != sequence_length):
                print("ERROR")
                break
              mega_file.write(sequence + "\n")
            elif (file == "utr_5_prime.fa"):
              five_prime_exons += 1
              sequence = str(myseq).lower()
              sequence = sequence[0] + sequence[1].upper() + sequence[2:]
              sequence = sequence[0:sequence_length]
              if (len(sequence) != sequence_length):
                print("ERROR")
                break
              mega_file.write(sequence + "\n")
            elif (file == "introns.fa"):
              introns += 1
              sequence = str(myseq).lower()
              sequence = sequence[100:len(sequence) - 100]
              diff = len(sequence) - sequence_length
              random = np.random.randint(diff, size=(1))
              random_num = random[0]
              sequence = sequence[random_num:sequence_length+random_num]
              if (len(sequence) != sequence_length):
                print("ERROR")
                break
              mega_file.write(sequence + "\n")
    
    print("Done creating imbalanced file. Listed below are the numbers of cds exons, five prime UTR exons, three prime UTR exons, and introns that are in the file")
    print(cds_exons, five_prime_exons, three_prime_exons, introns)
    mega_file.close()
    
    balanced_num_introns = max([cds_exons, five_prime_exons, three_prime_exons])
    mega_file_new = open("mega_balanced_file", "w+")
    sequence_length = length
    
    introns = 0
    cds_exons = 0
    five_prime_exons = 0
    three_prime_exons = 0
    
    #  This line is for when you're trying to create a balanced input file
    #  or (file == "introns.fa" and introns > NUMBER)
    
    for i in range (1, 5):
      fileDir = my_dir + str(i)
      files_to_parse = ["cds_exons.fa", "utr_3_prime.fa", "utr_5_prime.fa", "introns.fa"]
      for file in files_to_parse:
        fileName = fileDir + "/" + file
        for record in SeqIO.parse(fileName, "fasta"):
          myseq = record.seq
          if (str(myseq).count('N') > 0 or str(myseq).count('n') > 0 or len(myseq) <= sequence_length or (file == "introns.fa" and len(myseq) <= sequence_length + 200) or (file == "introns.fa" and introns > balanced_num_introns)):
            pass
          else:
            if (file == "cds_exons.fa"):
              cds_exons += 1
              sequence = str(myseq).upper()
              sequence = sequence[0:sequence_length]
              if (len(sequence) != sequence_length):
                print("ERROR")
                break
              mega_file_new.write(sequence + "\n")
            elif (file == "utr_3_prime.fa"):
              three_prime_exons += 1
              sequence = str(myseq).lower()
              sequence = sequence[0].upper() + sequence[1:]
              sequence = sequence[0:sequence_length]
              if (len(sequence) != sequence_length):
                print("ERROR")
                break
              mega_file_new.write(sequence + "\n")
            elif (file == "utr_5_prime.fa"):
              five_prime_exons += 1
              sequence = str(myseq).lower()
              sequence = sequence[0] + sequence[1].upper() + sequence[2:]
              sequence = sequence[0:sequence_length]
              if (len(sequence) != sequence_length):
                print("ERROR")
                break
              mega_file_new.write(sequence + "\n")
            elif (file == "introns.fa"):
              introns += 1
              sequence = str(myseq).lower()
              sequence = sequence[100:len(sequence) - 100]
              diff = len(sequence) - sequence_length
              random = np.random.randint(diff, size=(1))
              random_num = random[0]
              sequence = sequence[random_num:sequence_length+random_num]
              if (len(sequence) != sequence_length):
                print("ERROR")
                break
              mega_file_new.write(sequence + "\n")
    
    print("Done creating balanced file. Listed below are the numbers of cds exons, five prime UTR exons, three prime UTR exons, and introns that are in the file")
    print(cds_exons, five_prime_exons, three_prime_exons, introns)
    mega_file_new.close()
    
if __name__=="__main__":
    main()