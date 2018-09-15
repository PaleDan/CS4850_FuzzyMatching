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
	size_t distance;
	string value;
};

// prototype for levenshtein
size_t uiLevenshteinDistance( const std::string &s1, const std::string &s2);






// sort to use for vector that is filled with struct "Records", once sorted the lowest levenshtein distances should be easy to discern
bool sortByDistance (Record const & a, Record & b)
{
	return a.distance < b.distance;
}

// reads the the given file and stores its values in a vector
vector<string> readFile(ifstream& fileName)
{

	string line;
	vector<string>fileVector(100);
	int i = 0;

	if(fileName.is_open())
	{
		 while ( getline (fileName,line) )
			    {
			      fileVector [i] = line;
			      i++;

			    }
			    fileName.close();
	}

	return fileVector;
}

//** having trouble getting this to work but the idea is to pass a string input into the function and compare it with every string value in the file which is accessible through the vector it was copied to
vector<Record> compare (string input, vector<string> file)
{
	string temp;
	size_t temp2;
	Record temp3;
	vector<Record> records;

	for(size_t i = 0; i <= file.size(); i++)
	{
		temp = file[i];
		temp2 = uiLevenshteinDistance(input, temp);
		temp3.distance = temp2;
		temp3.value = temp;
		records[i] = {temp2, temp};
	}
	return records;
}




// actual function for calculating levenshtein distance
size_t uiLevenshteinDistance( const std::string &s1, const std::string &s2)
{
  const size_t m(s1.size());
  const size_t n(s2.size());

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

  return result;
}

int main()
{
	string input, line;

	// vector containing the strings from the file
	vector<string>fileVector(100);

	// vector containing
	vector<Record>sortedVector(100);


	// stores the given file in the variable myFile
	 std::ifstream myFile ("somefile.txt", std::ifstream::in);



	 // input
	cin >> input;

	// fills the fileVector with the strings from the file
	fileVector = readFile(myFile);


	//** function that insn't working
	sortedVector = compare(input, fileVector);



	// prints the contents of the fileVector to show that the strings from the file are copied to the vector
	for (auto i = fileVector.begin(); i != fileVector.end(); ++i)
			    std::cout << *i << ' ';






	cout << " End of program";





        return 0;
}
