/*********************************************
 *  Agent.java 
 *  Sample Agent for Text-Based Adventure Game
 *  COMP3411 Artificial Intelligence
 *  UNSW Session 1, 2017
*/

import java.util.*;
import java.io.*;
import java.net.*;
import java.util.Queue;
import java.util.LinkedList;

public class Agent {
   static final int EAST = 0;
   static final int NORTH = 1;
   static final int WEST = 2;
   static final int SOUTH = 3;
   private char map[][]=new char[201][201];
   private char[][] view;
   ArrayDeque<Object> used = new ArrayDeque();

   private int nrows;
   private int irow;
   private int icol;
   private int row;
   private int col;
   private int dirn;

   private boolean have_axe = false;
   private boolean have_key = false;
   private boolean have_raft = false;
   private boolean on_raft = false;
   private boolean off_map = false;
   private boolean game_won = false;
   private boolean game_lost = false;
   private boolean have_treasure = false;
   private int num_dynamites_held = 0;

   public void init_map(){
      for(int i=0; i < 201; i++ ) {
         for(int j=0; j < 201; j++ ) {
            this.map[i][j]=0;
         }
      }
   }

   public void forwrd_step(){
      switch(this.dirn) {
         case 0:
            this.irow=this.row;
            this.icol=this.col-1;
            break;
         case 1:
            this.irow=this.row-1;
            this.icol=this.col;
            break;
         case 2:
            this.irow=this.row;
            this.icol=this.col+1;
            break;
         case 3:
            this.irow=this.row+1;
            this.icol=this.col;
      }
   }

   public  void write_map(char view[][]){
      char temp[][]=new char[5][5];
      for(int  i=0; i < 5; i++ ) {
         for(int j=0; j < 5; j++ ) {
            switch(this.dirn) {
               case 0:
                  temp[j][4-i] = this.view[i][j];
                  break;
               case 1:
                  temp[i][j] = this.view[i][j];
                  break;
               case 2:
                  temp[j][4-i] = this.view[i][j];
                  break;
               case 3:
                  temp[4-i][4-j] = this.view[i][j];
            }
         }
      }
      this.map[row-1][col-1]=temp[row-1][col-1];
      this.map[row-1][col  ]=temp[row-1][col  ];
      this.map[row-1][col+1]=temp[row-1][col+1];
      this.map[row  ][col-1]=temp[row  ][col-1];
      this.map[row  ][col+1]=temp[row  ][col+1];
      this.map[row+1][col-1]=temp[row+1][col-1];
      this.map[row+1][col  ]=temp[row+1][col  ];
      this.map[row+1][col+1]=temp[row+1][col+1];
   }
   public void queue(int x, int y){


   }
   public void find_options(int x, int y){


   }

   public char get_action( char view[][] ) {

      // REPLACE THIS CODE WITH AI TO CHOOSE ACTION

      int ch=0;

      System.out.print("Enter Action(s): ");

      try {
         while ( ch != -1 ) {
            // read character from keyboard
            ch  = System.in.read();

            switch( ch ) { // if character is a valid action, return it
            case 'F': case 'L': case 'R': case 'C': case 'U': case 'B':
            case 'f': case 'l': case 'r': case 'c': case 'u': case 'b':
               return((char) ch );
            }
         }
      }
      catch (IOException e) {
         System.out.println ("IO error:" + e );
      }

      return 0;
   }

   void print_view( char view[][] )
   {
      int i,j;

      System.out.println("\n+-----+");
      for( i=0; i < 5; i++ ) {
         System.out.print("|");
         for( j=0; j < 5; j++ ) {
            if(( i == 2 )&&( j == 2 )) {
               System.out.print('^');
            }
            else {
               System.out.print( view[i][j] );
            }
         }
         System.out.println("|");
      }
      System.out.println("+-----+");
   }
   public void ret_action(){

   }
   public static void main( String[] args )
   {
      InputStream in  = null;
      OutputStream out= null;
      Socket socket   = null;
      Agent  agent    = new Agent();
      char   view[][] = new char[5][5];
      char   action   = 'F';
      int port;
      int ch;

      if( args.length < 2 ) {
         System.out.println("Usage: java Agent -p <port>\n");
         System.exit(-1);
      }

      port = Integer.parseInt( args[1] );

      try { // open socket to Game Engine
         socket = new Socket( "localhost", port );
         in  = socket.getInputStream();
         out = socket.getOutputStream();
      }
      catch( IOException e ) {
         System.out.println("Could not bind to port: "+port);
         System.exit(-1);
      }

      try { // scan 5-by-5 wintow around current location
         while( true ) {
            for(int i=0; i < 5; i++ ) {
               for(int j=0; j < 5; j++ ) {
                  if( !(( i == 2 )&&( j == 2 ))) {
                     ch = in.read();
                     if( ch == -1 ) {
                        System.exit(-1);
                     }
                     view[i][j] = (char) ch;
                  }
               }
            }
            agent.print_view( view ); // COMMENT THIS OUT BEFORE SUBMISSION
            action = agent.get_action( view );
            out.write( action );
         }
      }
      catch( IOException e ) {
         System.out.println("Lost connection to port: "+ port );
         System.exit(-1);
      }
      finally {
         try {
            socket.close();
         }
         catch( IOException e ) {}
      }
   }
}
