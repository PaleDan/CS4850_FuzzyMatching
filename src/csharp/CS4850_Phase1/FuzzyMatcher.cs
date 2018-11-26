using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace CS4850_Phase1
{
    public enum StringAlgorithms
    {
        LevenshteinDistance,
        SmithWaterman
        //add more as needed
    }

    class FuzzyMatcher
    {


        #region Fields
        private static readonly Dictionary<StringAlgorithms, Delegate> algorithms;
            

        #region Delegates
        private delegate int DelGetLevenshteinDistance(String s, String t);
        private delegate int DelSmithWaterman(String s, String t);
        #endregion Delegates 
        #endregion Fields

        #region Methods

        //static constructor
        static FuzzyMatcher()
        {
            algorithms = new Dictionary<StringAlgorithms, Delegate>
            {
                { StringAlgorithms.LevenshteinDistance, new DelGetLevenshteinDistance(GetLevenshteinDistance) }
            };
        }

        /// <summary>
        /// Calculates the 
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="query">the query string</param>
        /// <param name="database">the </param>
        /// <param name=""></param>
        /// <returns></returns>
        public static IList<KeyValuePair<String, T>> GetAllDistanecs<T>(String query, IList<String> database, StringAlgorithms algorithm = StringAlgorithms.LevenshteinDistance)
        {
            return FindClosestMatches<T>(query, database, database.Count, algorithm);
        }



        /// <summary>
        /// Finds the specified number of the top closest matches between the
        /// query string and the database of strings to be matched against. The
        /// matching algorithm to be used is an optional parameter of
        /// the StringAlgorithms enum type; if no StringAlgorithms 
        /// argument is passed in, it will default to Levenshtein distance.
        /// </summary>
        /// <typeparam name="T">the data type of the metric being used by the
        /// specified string similarity algorithm. If no algorithm is
        /// specified, this method will default to Levenshtein distance which
        /// uses an integer edit distance metric.
        /// </typeparam>
        /// <param name="query">the query string</param>
        /// <param name="database">database of strings to be matched against</param>
        /// <param name="numMatches">number of closest matches to be returned</param>
        /// <param name="algorithm"></param>
        /// <returns></returns>
        public static IList<KeyValuePair<String, T>> FindClosestMatches<T>(String query, IList<String> database, int numMatches, StringAlgorithms algorithm = StringAlgorithms.LevenshteinDistance) 
        {
            IList<KeyValuePair<String, T>> result = new List<KeyValuePair<String, T>>(numMatches);
            
            return result;
        }


        /// <summary>
        /// Matches a query string against a database of strings stored in the
        /// specified file, using the specified algorithm, and returns the the top
        /// 'numMatches' number of closest-matching strings found.
        /// </summary>
        /// <typeparam name="T">the data type of the metric being used by the
        /// specified string similarity algorithm. If no algorithm is
        /// specified, this method will default to Levenshtein distance which
        /// uses an integer edit distance metric.
        /// </typeparam>
        /// <param name="query">the query string; the string to be matched</param>
        /// <param name="fileName">the name of the file containing the data
        /// set to be matched against
        /// </param>
        /// <param name="numMatches">the number of closest matches to be found
        /// </param>
        /// <param name="algorithm">the string algorithm to be used to do the
        /// matching
        /// </param>
        /// <returns>a List (as an IList) of the closest matches to the query
        /// string and the corresponding string similarity metric value, stored
        /// as (key, value) pairs with the matched string as the key and the
        /// metric as the value.
        /// </returns>
        public static IList<KeyValuePair<String, T>> FindClosestMatches<T>(String query, String fileName, int numMatches, StringAlgorithms algorithm = StringAlgorithms.LevenshteinDistance)
        {
            
            IList<KeyValuePair<String, T>> result = new List<KeyValuePair< String, T>> (numMatches);
            
            try
            {
                string line;
                using (StreamReader sr = new StreamReader(fileName))
                {
                    while ((line = sr.ReadLine()) != null)
                    {
                        result.Add(new KeyValuePair<String, T> (line, (T)algorithms[algorithm].DynamicInvoke(new Object[] { query, line } )));
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

            return result;
        }

        /// <summary>
        /// Calculates the Levenshtein distance between two strings.
        ///
        /// This implementation was taken from rosettacode.org, which is under
        /// the GNU Free Documentation License 1.2
        /// Copyright (C) 2000,2001,2002  Free Software Foundation, Inc.
        /// 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
        /// Everyone is permitted to copy and distribute verbatim copies
        /// of this license document, but changing it is not allowed.
        /// </summary>
        /// <param name="source"></param>
        /// <param name="target"></param>
        /// <returns></returns>
        public static int GetLevenshteinDistance(string s, string t)
        {
            int n = s.Length;
            int m = t.Length;
            int[,] d = new int[n + 1, m + 1]; //array of substring levenshtein distances

            if (n == 0)
            {
                return m;
            }

            if (m == 0)
            {
                return n;
            }

            for (int i = 0; i <= n; i++)
                d[i, 0] = i;
            for (int j = 0; j <= m; j++)
                d[0, j] = j;

            for (int j = 1; j <= m; j++)
                for (int i = 1; i <= n; i++)
                    if (s[i - 1] == t[j - 1])
                        d[i, j] = d[i - 1, j - 1];  //no operation
                    else
                        d[i, j] = Math.Min(Math.Min(
                            d[i - 1, j] + 1,    //a deletion
                            d[i, j - 1] + 1),   //an insertion
                            d[i - 1, j - 1] + 1 //a substitution
                            );

            //double similarityPercentage = ((1.0 - (d[n, m] / (double)Math.Max(s.Length, t.Length))));
            return d[n, m];
        }
        #endregion Methods
    }
}
