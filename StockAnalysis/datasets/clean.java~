import java.io.*;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;

class Clean
{ // start clean
public static void main(String args[]) throws IOException
{ // main st
BufferedReader br = null;
String a=new String();
String b=new String();
String c=new String();
File file1 = new File("/home/admin/PycharmProjects/nse_mapping.txt");
File file2 = new File("/home/admin/PycharmProjects/bse_mapping.txt");
// if file doesnt exists, then create it
if (!file1.exists()) {
				file1.createNewFile();
			}

			FileWriter fw1 = new FileWriter(file1.getAbsoluteFile());
if (!file2.exists()) {
				file2.createNewFile();
			}

			FileWriter fw2 = new FileWriter(file2.getAbsoluteFile());		
try 
{ // try st
String s;
br = new BufferedReader(new FileReader("/home/admin/PycharmProjects/StockAnalysis/datasets/companies.txt"));
while ((s = br.readLine()) != null)
{ //while st
StringBuffer sb=new StringBuffer();
for(int i=0;i<=s.length()-6;i++)
{ //for st
if(Character.isDigit(s.charAt(i))&&Character.isDigit(s.charAt(i+1))&&Character.isDigit(s.charAt(i+2))&&Character.isDigit(s.charAt(i+3))&&Character.isDigit(s.charAt(i+4))&&Character.isDigit(s.charAt(i+5)))
{ // if st
sb.append(s.substring(0,i));
sb.append(',');
sb.append(s.substring(i,6+i));
if((i+6)!=s.length()) // nse
{ //if st
sb.append(',');
sb.append(s.substring(i+6,s.length()));
sb.append('\n');
BufferedWriter bw1 = new BufferedWriter(fw1);
bw1.write(sb.toString());
bw1.flush();
} // if end
else
{
sb.append('\n');
System.out.println(sb);
BufferedWriter bw2 = new BufferedWriter(fw2);
bw2.write(sb.toString());
bw2.flush();
}
} // if end
}
 // for end


//close the stream

} // while end
/*
int i=0;
while(!Character.isDigit(sCurrentLine.charAt(i)))
i++;
a=sCurrentLine.substring(0,i);
StringBuffer sb=new StringBuffer();
sb.append(a);
sb.append(',');
b=sCurrentLine.substring(i,6+i);
sb.append(b);
if((6+i)==sCurrentLine.length())
continue;
else
c=sCurrentLine.substring(i+6,sCurrentLine.length());
sb.append(c);
System.out.println(sCurrentLine);
System.out.println(sb);
*/
} //try end
catch (IOException e) 
{
e.printStackTrace();
} 
finally 
{ //finally st
try 
{ 
if (br != null)br.close();
} 
catch (IOException ex) 
{
ex.printStackTrace();
}
} // final end
} // main end
} // end clean
