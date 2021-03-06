#include <string>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <iterator>
#include <array>
#include <vector>

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

//** having trouble getting this to work but the idea is to pass a string input into the function and compare it with every string value in the file which is accessible through the vector it was copied to
vector<Record> compare(string input, vector<string> file)
{
    vector<Record> results;
    Record result;
    for(int i = 0; i < file.size(); i++)
    {
        float distance = uiLevenshteinDistance(input, file[i]);
        if (distance > result.distance) 
        {
            result.distance = distance;
            result.value = file[i];
        }
    }
    results.push_back(result);
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
    string input;

    // stores the given file in the variable myFile
    std::ifstream myFile("somefile.txt", std::ifstream::in);

    // input
    std::getline(std::cin, input);

    // fills the fileVector with the strings from the file
    vector<string> fileVector = readFile(myFile);

    //** function that insn't working
    vector<Record> sortedVector = compare(input, fileVector);

    // prints the contents of the fileVector to show that the strings from the file are copied to the vector
    for (int i = 0; i < sortedVector.size(); i++) {
        std:cout << sortedVector[i].value << " : " << sortedVector[i].distance << "\n";
    }

    cout << " End of program";
    cin >> input;

    return 0;
}