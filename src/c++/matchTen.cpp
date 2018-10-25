#include <string>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <iterator>
#include <array>
#include <vector>
#include <thread>
#include <future>
#include <functional>

using namespace std;

// struct type that stores two data type variables, in this case the LevenshteinDistance and the string your input was compared with in the file
template<class ASYNC>
struct Record
{
	float distance;
	ASYNC value;
};

// prototype for levenshtein
float uiLevenshteinDistance(const std::string &s1, const std::string &s2);


// function for sorting the final vector
void finalSort(vector<Record> finalVector)
{
	Record result;
	 result.distance = finalVector[0].distance;
	 result.value = finalVector[0].value;

	 for (int i = 1; i > finalVector.size(); i++)
	 {
		 if (result.distance < finalVector[i].distance)
		 {
			 result.distance = finalVector[i].distance;
			 result.value = finalVector[i].value;
		 }

		 
	}
	 cout << "The closest match is:" << result.value << " which has a levenshtein distance of " << result.distance <<"::::::";

}

// function to get the number of lines in a file
int fileLines(ifstream& file)
{
	int number_of_Lines = 0;
	string line;

	if (file.is_open()) {
		while (std::getline(file, line))
		{
			++number_of_Lines;
		}
		file.close();
	}
			
	
		
	std::cout << "The number of lines in the file is: " << number_of_Lines << endl;
	return number_of_Lines;
}

// reads the the given file and stores its values in a vector
vector<string> readFile0(ifstream& file)
{
	string line;
	vector<string>fileVector0;

	cout << "thread 0 is starting..." << endl;

	if (file.is_open())
	{
		for (int i = 1; !file.eof(); i + 4)
		{
			getline(file, line);
			fileVector0.push_back(line);

		}
		file.close();

	}
	cout << "thread 0 is complete..." << endl;
	return fileVector0;
}

vector<string> readFile1(ifstream& file)
{
	string line;
	vector<string>fileVector1;

	cout << "thread 1 is starting..." << endl;

	if (file.is_open())
	{
		for(int i = 1; !file.eof(); i + 4)
		{
			getline(file, line);
			fileVector1.push_back(line);
			
		}
		file.close();

	}
	cout << "thread 1 is complete..." << endl;
	return fileVector1;
}

vector<string> readFile2(ifstream& file)
{
	string line;
	vector<string>fileVector2;

	cout << "thread 2 is starting..." << endl;

	if (file.is_open())
	{
		for(int i = 2; !file.eof(); i + 4)
		{
			getline(file, line);
			fileVector2.push_back(line);
			
		}
		file.close();

	}
	cout << "thread 2 is complete..." << endl;
	return fileVector2;
}

vector<string> readFile3(ifstream& file)
{
	string line;
	vector<string>fileVector3;

	cout << "thread 3 is starting..." << endl;

	if (file.is_open())
	{
		for(int i = 3; !file.eof(); i + 4)
		{
			getline(file, line);
			fileVector3.push_back(line);
		
		}
		file.close();

	}
	cout << "thread 3 is complete..." << endl;
	return fileVector3;
}

// compares the input given by the user to the files lines stored in the vector
template<class ASYNC>
vector<Record> compare(string input, ASYNC &file)
{
	vector<Record> results;
	Record result;
	for (int i = 0; i < file.size(); i++)
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
float uiLevenshteinDistance(const std::string &s1, const std::string &s2)
{
	const size_t m(s1.size());
	const size_t n(s2.size());
	const size_t sum = m + n;

	if (m == 0) return n;
	if (n == 0) return m;

	size_t *costs = new size_t[n + 1];

	for (size_t k = 0; k <= n; k++) costs[k] = k;

	size_t i = 0;
	for (std::string::const_iterator it1 = s1.begin(); it1 != s1.end(); ++it1, ++i)
	{
		costs[0] = i + 1;
		size_t corner = i;

		size_t j = 0;
		for (std::string::const_iterator it2 = s2.begin(); it2 != s2.end(); ++it2, ++j)
		{
			size_t upper = costs[j + 1];
			if (*it1 == *it2)
			{
				costs[j + 1] = corner;
			}
			else
			{
				size_t t(upper < corner ? upper : corner);
				costs[j + 1] = (costs[j] < t ? costs[j] : t) + 1;
			}

			corner = upper;
		}
	}

	size_t result = costs[n];
	delete[] costs;

	return (sum - result) * 1.0 / sum;
}

int main()
{
	Record result0, result1, result2, result3, finalResult;
	string input, fileName;
	int number_Of_Lines;
	vector<Record> finalVector;

	// stores the given file in the variable myFile
	cout << "Please enter a file name to read:" << endl;
	std::getline(std::cin, fileName);
	std::ifstream myFile(fileName, std::ifstream::in);

	// input for comparison with file results
	cout << "Please enter a record name for comparison:" << endl;
	std::getline(std::cin, input);

	/* fills the fileVector with the strings from the file with every fourth line of the file starting at 0, the function is run concurrently with it's likewise 
	*I had to use auto to simulate the vector type here because using async created a special type that can't be stored using by simply using a string vector
	*/
	auto t1 = async(launch::async, readFile0, ref(myFile));

	
	auto t2 = async(launch::async, readFile1, ref(myFile));

	
	auto t3 = async(launch::async, readFile2, ref(myFile));

	
	auto t4 = async(launch::async, readFile3, ref(myFile))

	// produces levenshtein values by comparing the input with the first 1/4 of the file (here is where I'm having trouble because the Record vector can't store the new type.
	// using auto here wouldn't work either because you need to create a struct to idenify the closest levenshtein distance and the string match associated with it.
	vector<Record> sortedVector0 = compare(input, t1);

	// produces levenshtein values by comparing the input with the second 1/4 of the file
	vector<Record> sortedVector1 = compare(input, t2);

	// produces levenshtein values by comparing the input with the third 1/4 of the file
	vector<Record> sortedVector2 = compare(input, t3);

	// produces levenshtein values by comparing the input with the final 1/4 of the file
	vector<Record> sortedVector3 = compare(input, t4);

	// here I'm simply merging the values of the four vectors created from the four parts of the file into one 
	result0.value = sortedVector0[0].value;
	result0.distance = sortedVector0[0].distance;
	finalVector.push_back(result0);

	result1.value = sortedVector1[0].value;
	result1.distance = sortedVector1[0].distance;
	finalVector.push_back(result1);

	result2.value = sortedVector2[0].value;
	result2.distance = sortedVector2[0].distance;
	finalVector.push_back(result2);

	result3.value = sortedVector3[0].value;
	result3.distance = sortedVector3[0].distance;
	finalVector.push_back(result3);

	// sorts the four values of the finalVector (assuming that we decide to print more values from the threads, a more efficient sort could be utilized here).
	finalSort(finalVector);

	std::cout << " End of program";

	return 0;
}
