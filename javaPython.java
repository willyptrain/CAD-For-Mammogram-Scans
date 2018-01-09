import java.io.*;
import java.awt.*;  
import javax.swing.*;  

public class javaPython {  
   public javaPython()  
   {  
      JFrame f= new JFrame("Panel Example");    
      JPanel panel=new JPanel();  
      panel.setBounds(40,80,200,200);    
      panel.setBackground(Color.BLACK);  
      f.add(panel);  
      f.setSize(400,400);    
      f.setLayout(null);    
      f.setVisible(true);    
   }  
   public static void main(String args[])  
   {  
   String s = null;

        try {
            
            new javaPython();
             
            Process p = Runtime.getRuntime().exec("python NNpython.py");
            
            BufferedReader in = new BufferedReader(
                                new InputStreamReader(p.getInputStream()));
            String line = null;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
            
            
            
        }
        catch (IOException e) {
            System.out.println("error");
        }

      new javaPython();  
   }  
}  