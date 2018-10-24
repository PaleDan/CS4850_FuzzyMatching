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

    struct Match
    {
        /// <summary>
        /// 
        /// </summary>
        public int RowIndex { get; set; }
        /// <summary>
        /// 
        /// </summary>
        public String Source { get; set; }
        /// <summary>
        /// 
        /// </summary>
        public String Lookup { get; set; }
        /// <summary>
        /// 
        /// </summary>
        public double SimilarityRatio { get; set; }

        public Match(String source, String lookup, double similarityRatio, int rowIndex = -1)
        {
            RowIndex = rowIndex;
            Source = source;
            Lookup = lookup;
            SimilarityRatio = similarityRatio;
        }
    }

    class FuzzyMatcher
    {
        #region Fields
        #endregion Fields

        #region Methods
        //TODO: rename 'GetAllDistances' to something more appropriate
        /// <summary>
        /// Calculates the Levenshtein distances between the query string
        /// and every string in some database.
        /// </summary>
        /// <param name="query">the query string</param>
        /// <param name="database">database of strings to be matched against
        /// </param>
        /// <returns>an IList of matches; each match contains a string 
        /// similarity ratio calculated from an associated Levenshtein distance
        /// </returns>
        public static IList<Match> GetAllDistances(String query, IList<String> database)
        {
            return FindClosestMatches(query, database, database.Count);
        }

        /// <summary>
        /// Finds the specified number of the top closest matches between the
        /// query string and the database of strings to be matched against.
        /// </summary>
        /// <param name="query">the query string</param>
        /// <param name="database">database of strings to be matched against
        /// </param>
        /// <param name="numMatches">number of closest matches to be returned
        /// </param>
        /// <returns></returns>
        public static IList<Match> FindClosestMatches(String query, IList<String> database, int numMatches)
        {
            List<Match> matches = new List<Match>(numMatches);

            for (int i = 0; i < database.Count; ++i)
            {
                matches.Add(new Match(query, database[i], GetLevenshteinRatio(query, database[i]), i));
            }

            matches.Sort((m1, m2) => -1 * m1.SimilarityRatio.CompareTo(m2.SimilarityRatio));
            return matches.Take(numMatches).ToList();
        }

        /// <summary>
        /// Matches a query string against a database of strings stored in the
        /// specified file and returns the the top
        /// 'numMatches' number of closest-matching strings found.
        /// </summary>
        /// <param name="query">the query string; the string to be matched</param>
        /// <param name="fileName">the name of the file containing the data
        /// set to be matched against
        /// </param>
        /// <param name="numMatches">the number of closest matches to be found
        /// </param>
        /// <returns>an IList of the closest matches to the query string
        /// </returns>
        public static IList<Match> FindClosestMatches(String query, String fileName, int numMatches)
        {
            List<Match> result = new List<Match>();
            //TODO: use a BST or other sorted data structure to reduce overhead
            //      of maintaining the current top 'numMatches' # of matches
            //double currentLowestSimilarity = 0.0f;

            try
            {
                string line;
                int lineNum = 0;
                using (StreamReader sr = new StreamReader(fileName))
                {
                    while ((line = sr.ReadLine()) != null)
                    {
                        result.Add(new Match(query, line, GetLevenshteinRatio(query, line), lineNum));
                        ++lineNum;
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

            result.Sort((m1, m2) => -1 * m1.SimilarityRatio.CompareTo(m2.SimilarityRatio));
            return result.Take(numMatches).ToList();
        }

        /// <summary>
        /// Finds a list of matches whose similarity ratios are above the 
        /// specified threshold
        /// </summary>
        /// <param name="query">the query string</param>
        /// <param name="fileName">the name of the file containing the set of
        /// strings to be matched against
        /// </param>
        /// <param name="threshold">the similarity threshold</param>
        /// <returns>a list of matches whose similarity ratios are above the 
        /// specified threshold
        /// </returns>
        public static IList<Match> FindMatchesAboveThreshold(String query, String fileName, double threshold)
        {
            if (threshold < 0)
            {
                throw new ArgumentOutOfRangeException("threshold must be greater than or equal to 0");
            }
            List<Match> result = new List<Match>();

            try
            {
                string line;
                int lineNumber = 0;
                using (StreamReader sr = new StreamReader(fileName))
                {
                    while ((line = sr.ReadLine()) != null)
                    {
                        Match currentMatch = new Match(query, line, GetLevenshteinRatio(query, line), lineNumber);
                        if (currentMatch.SimilarityRatio >= threshold)
                        {
                            result.Add(currentMatch);
                        }
                        ++lineNumber;
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

            return d[n, m];
        }

        //TODO?: can add a 'Distance' or 'SimilarityMetric' property to the
        //      Match struct to simplify the means by which we convert or
        //      normalize the Levenshtein distance into a ratio
        /// <summary>
        /// Calculates the similarity ratio associated with the Levenshtein
        /// distance between the two specified strings
        /// </summary>
        /// <param name="s">source string</param>
        /// <param name="t">target string</param>
        /// <returns>similarity ratio associated with the Levenshtein
        /// distance between the two specified strings</returns>
        public static double GetLevenshteinRatio(String s, String t)
        {
            return ((1.0d - (GetLevenshteinDistance(s, t) / (double)Math.Max(s.Length, t.Length))));
        }
        #endregion Methods
    }
}
