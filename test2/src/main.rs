extern crate serde;
#[macro_use]
extern crate serde_derive;
extern crate serde_json;

use std::fs::File;
use std::io;
use std::io::prelude::*;

use serde::{ Deserialize, Serialize };
use serde_json::Result;

#[derive(Clone, Debug, Serialize, Deserialize)]
enum WordType {
    Verb,
    Noun,
}

#[derive(Debug, Serialize, Deserialize)]
struct Entry {
    index: usize,
    text: String,
    text_type: WordType,
    leads_to: Option<usize>,
}
impl Entry {
    pub fn new(index:usize, text:String, text_type:WordType, leads_to:Option<&usize>) -> Entry {
        let leads_to = match leads_to {
            Some(i) => Some(*i),
            None => None,
        };
        Entry {
            index,
            text,
            text_type,
            leads_to,
        }
    }
}

#[derive(Serialize, Deserialize)]
struct Chain {
    entries: Vec<Vec<Entry>>
}
impl Chain {
    pub fn new() -> Chain {
        Chain {
            entries: vec![]
        }
    }
}

fn main() {
    let mut verbs_file = File::open("verblist.txt").unwrap();
    let mut raw_verbs = String::new();
    verbs_file.read_to_string(&mut raw_verbs).unwrap();
    let verbs = raw_verbs.split("\n").filter(|verb| !verb.is_empty())
                                     .map(|verb| String::from(verb.to_lowercase()
                                                                  .trim()
                                                              ))
                                     .collect::<Vec<String>>();

     let mut nouns_file = File::open("nounlist.txt").unwrap();
     let mut raw_nouns = String::new();
     nouns_file.read_to_string(&mut raw_nouns).unwrap();
     let nouns = raw_nouns.split("\n").filter(|noun| !noun.is_empty())
                                      .map(|noun| String::from(noun.to_lowercase()
                                                                   .trim()
                                                               ))
                                      .collect::<Vec<String>>();

    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();

    let mut sentence_chains = vec![];

    for sentence in input.to_lowercase().split(".") {
        let mut pre_words = vec![];
        let mut pre_chain = vec![];
        for word in sentence.split(" ") {
            let word = word.trim();
            if verbs.iter().any(|verb| verb == word) || nouns.iter().any(|noun| noun == word) {
                let mut x = pre_words.clone();
                pre_words = vec![];
                x.push(String::from(word));
                pre_chain.push(x);
            } else if !word.is_empty() {
                pre_words.push(String::from(word));
            }
        }
        if !pre_words.is_empty() {
            pre_chain.push(pre_words);
        }
        sentence_chains.push(pre_chain);
    }

    let mut output_chains = Chain::new();
    for pre_chain in sentence_chains {
        let mut c = vec![];
        let mut noun_indexes = vec![];
        let mut verb_indexes = vec![];
        let mut entries = vec![];
        for (i, entry) in pre_chain.iter().enumerate() {
            // println!("{}", entry.join(" "));
            let determiner = &entry[entry.len() - 1];
            let word_type = if verbs.iter().any(|verb| verb == determiner) {
                verb_indexes.push(i);
                WordType::Verb
            } else {
                noun_indexes.push(i);
                WordType::Noun
            };
            let text = entry.iter()
                            .filter(|word| (*word).chars()
                                                  .any(|ch| ch.is_alphabetic())
                                   )
                            .map(|word| word.clone())
                            .collect::<Vec<String>>()
                            .join(" ");
            c.push((text, word_type));
        }
        for (i, (text, word_type)) in c.iter().enumerate() {
            let leads_to = match word_type {
                WordType::Verb => noun_indexes.iter().skip_while(|vi| **vi < i).next(),
                WordType::Noun => verb_indexes.iter().skip_while(|vi| **vi < i).next()
            };
            entries.push(Entry::new(i, text.to_string(), (*word_type).clone(), leads_to));
        }
        // println!("{:?}", entries);
        output_chains.entries.push(entries);
    }
    println!("{}", serde_json::to_string(&output_chains).unwrap());
    // println!("{}", input);
}
