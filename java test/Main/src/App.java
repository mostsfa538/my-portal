import java.util.Scanner;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
public class App {
    static Scanner in = new Scanner(System.in);
    static String stringAdd(String s , String s1)
    {
        StringBuilder temp = new StringBuilder();
        int index =0;
        int index2 = 0;
        for(int i = 0 ; i <= s.length() + s1.length(); i++)
        {
            if(i % 2 == 0  && index2 < s.length())
            {
                temp.append(s.charAt(index2++));
            }
            else if ( i % 2 != 0  && index < s1.length())
            {
                temp.append(s1.charAt(index++));
            }
            else if(index == s1.length() && index2 < s.length())
            {
                temp.append(s.charAt(index2++));
            }
            else if(index2 == s.length() && index < s1.length())
            {
                temp.append(s1.charAt(index++));
            }
        }
        return temp.toString();
    }
    static StringBuilder trim(String s)

    {
        StringBuilder temp = new StringBuilder("");
        for(int i = 0 ;i <  s.length() ; i++)
        {
            if(i == 0  && s.charAt(i) == ' ')
            {
                continue;
            }
            boolean beforeFlag = false , afterFlag = false;
            if(s.charAt(i) != ' ')
            {
                temp.append(s.charAt(i));
            }
            else
            {
                for(int j = i-1 ; j >=0 ; j--)
                {
                    if(s.charAt(j) != ' ')
                    {
                        beforeFlag = true;
                        break;
                    }
                }
                for(int j = i+1 ; j < s.length() ; j++)
                {
                    if(s.charAt(j) != ' ')
                    {
                        afterFlag = true;
                        break;
                    }
                }
                if(beforeFlag && afterFlag)
                {
                    temp.append(s.charAt(i));
                }
            }
        }
        return temp;
    }
    static String removeChar(String s , char c)
    {
        String temp = "";
        for(int i = 0 ; i < s.length() ; i++)
        {
            if(s.charAt(i) != c)
            {
                temp += s.charAt(i);
            }
        }
        return temp;
    }
    static String duplicateChar(String s, char c)
    {
        String  temp = "";
        for(int i = 0 ; i < s.length() ; i++)
        {
            if(s.charAt(i) == c)
            {
                temp +=c;
                temp +=c;
            }
            else
            {
                temp += s.charAt(i);
            }
        }
        return temp;
    }
    static String  duplicateString(String s)
    {
        String temp = "";
        for(int i = 0 ; i< s.length() ; i++)
        {
            temp = temp + s.charAt(i) + s.charAt(i);
        }
        return temp;
    }
    static boolean endWith(String s , String substring)
    {
        int lengthOfString = s.length()-1 , lengthOfSubstring = substring.length()-1;
        String temp = "";
        for(int i =lengthOfString - lengthOfSubstring ; i < s.length() ;i++ )
        {
            temp += s.charAt(i);
        }
        return substring.equals(temp);
    }
    static boolean startWith(String s , String substring)
    {
        int lengthOfString = s.length()-1 , lengthOfSubstring = substring.length()-1;
        String temp = "";
        for(int i =0 ; i < lengthOfString - lengthOfSubstring ;i++ )
        {
            temp += s.charAt(i);
        }
        return substring.equals(temp);
    } 
    static String[] split(String s)
    {
        int wordsCounter = 0;
        for(int i = 0 ; i < s.length() ; i++)
        {
            if(s.charAt(i) == ' ')
            {
                wordsCounter++;
            }
        }
        s += " ";
        String[] temp = new String[wordsCounter+1];
        int independentIndex =0;
        for(int i = 0 ; i < s.length() ; i++)
        {
            String sumString = "";
            for(int j = i ; j < s.length() ; j++)
            {
                if(s.charAt(j) == ' ')
                {
                    i = j;
                    break;
                }
                else
                {
                    sumString +=s.charAt(j);
                }
            }
            temp[independentIndex++] = sumString;
            sumString = "";
        }
        return temp;
    }
    static String arrayOfCharsToStr(char[] c)
    {
        String temp ="";
        for(char i : c )
        {
            temp += i;
        }
        return temp;
    }
    static char[] strToArrayofChars(String s)
    {
        int strlen = s.length();
        char[] str = new char[strlen];
        for(int i = 0 ; i < s.length() ; i++)
        {
            str[i] = s.charAt(i);
        }
        return str;
    }
    static int countChar(String s, char c )
    {
        int counter = 0 ;
        for(int i = 0 ; i < s.length(); i++)
        {
            if(s.charAt(i) == 'c')
            {
                counter++;
            }
        }
        return counter;
    }


    public static void main(String[] args) throws Exception {
        File file = new File("C:\\Users\\mosta\\.vscode\\java test\\Main\\createdFile.txt");
        //Reader classes in java 
        Scanner fileScanner = new Scanner(file);
        FileReader fr = new FileReader(file);
        BufferedReader bufferedReader = new BufferedReader(fr);
        while(fileScanner.hasNextLine())
        {
            System.out.println(fileScanner.nextLine());
        }
        fileScanner.close();


        //Writer classes in java
        //FileWriter fw = new FileWriter(file,true);
        //BufferedWriter bufferedWriter = new BufferedWriter(fw);
        //PrintWriter printWriter = new PrintWriter(fw);



        //bufferedWriter.newLine();
        //bufferedWriter.close();
        bufferedReader.close();
    }
}
