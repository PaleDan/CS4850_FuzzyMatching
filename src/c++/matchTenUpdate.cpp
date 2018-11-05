#include <string>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <iterator>
#include <array>
#include <vector>
#include <math.h>
#include <chrono>  // for high_resolution_clock

using namespace std;

// struct type that stores two data type variables, in this case the LevenshteinDistance and the string your input was compared with in the file
struct Record
{
    float distance;
    string value;
};

// prototype for levenshtein
float uiLevenshteinDistance( const std::string &s1, const std::string &s2);

// sort to use for vector that is filled with struct "Records", once sorted the lowest levenshtein distances should be easy to discern
bool sortByDistance (Record const & a, Record & b)
{
    return a.distance < b.distance;
}

// reads the the given file and stores its values in a vector
vector<string> readFile(ifstream& file)
{
    string line;
    vector<string>fileVector;

    if(file.is_open())
    {
        while ( getline (file, line) )
        {
            fileVector.push_back(line);
        }
        file.close();
    }

    return fileVector;
}

//pass a string input into the function and compare it with every string value in the file which is accessible through the vector it was copied to
vector<Record> compare(string input, vector<string> file)
{
    vector<Record> results;
    Record result;
    for(int i = 0; i < file.size(); i++)
    {
        float distance = uiLevenshteinDistance(input, file[i]);
        result.distance = distance;
        result.value = file[i];
        results.push_back(result);
    }
    return results;
}

// actual function for calculating levenshtein distance
float uiLevenshteinDistance( const std::string &s1, const std::string &s2)
{
  const size_t m(s1.size());
  const size_t n(s2.size());
  const size_t sum = m + n;

  if( m==0 ) return n;
  if( n==0 ) return m;

  size_t *costs = new size_t[n + 1];

  for( size_t k=0; k<=n; k++ ) costs[k] = k;

  size_t i = 0;
  for ( std::string::const_iterator it1 = s1.begin(); it1 != s1.end(); ++it1, ++i )
  {
    costs[0] = i+1;
    size_t corner = i;

    size_t j = 0;
    for ( std::string::const_iterator it2 = s2.begin(); it2 != s2.end(); ++it2, ++j )
    {
      size_t upper = costs[j+1];
      if( *it1 == *it2 )
      {
          costs[j+1] = corner;
      }
      else
      {
        size_t t(upper<corner?upper:corner);
        costs[j+1] = (costs[j]<t?costs[j]:t)+1;
      }

      corner = upper;
    }
  }

  size_t result = costs[n];
  delete [] costs;

  return (sum - result) * 1.0 / sum;
}

int main()
{
    string input, fileName;
    int inputLengths = 10; 
    int funcInput;

    // stores the given file in the variable myFile
    cout << "Please enter a file name to read:" ;
    cin >> fileName;
    std::ifstream myFile(fileName, std::ifstream::in);

    // input
    //std::getline(std::cin, input);
   // cout << "Please enter the input string:" ;
   // cin>>input;
   //input = string(10, 'a');

    // fills the fileVector with the strings from the file
    vector<string> fileVector = readFile(myFile);

    while(inputLengths<=100){
    //** function that insn't working
    //** It is working now
    // Record start time
    funcInput = pow(inputLengths, 2);
    input = string(funcInput, 'a');
    inputLengths++;
    auto start = std::chrono::high_resolution_clock::now();
    vector<Record> sortedVector = compare(input, fileVector);
    // Record end time
    auto finish = std::chrono::high_resolution_clock::now();
/*
    // prints the contents of the fileVector to show that the strings from the file are copied to the vector
    for (int i = 0; i < sortedVector.size(); i++) {
        std:cout << sortedVector[i].value << " : " << sortedVector[i].distance << "\n";
    }
    */

    chrono::duration<double> elapsed = finish - start;
    cout<<"---------------------------------------"<<endl;
    cout<<"Length of input string :  "<<input.length()<<"\n";
    //cout<<"Input: " <<input<<"\n";
    cout<<"Size of the file       :  "<<fileVector.size()<<"\n";
    cout<<"Elapsed time           :  "<<elapsed.count() << " s\n";
    cout<<"---------------------------------------\n";

    }
    cout << "End of Benchmarking\n";
    //cin >> input;

    return 0;
}