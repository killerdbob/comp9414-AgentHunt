
/*********************************************
 *  Agent.java 
 *  Sample Agent for Text-Based Adventure Game
 *  COMP3411 Artificial Intelligence
 *  UNSW Session 1, 2017
 */

import java.util.*;
import java.awt.Point;
import java.io.*;
import java.net.*;

class Mark {
    public static final char HOME = 'H';
};

class MapGrid {
    public static final int MAX_SIZE = 180; 
    public char gridmap[][];
    public Point treasurePos;
    public Point startPos;

    public MapGrid(Point pos) {
        treasurePos = null;
        startPos = pos;
        gridmap = new char[MAX_SIZE][MAX_SIZE];
        for (int i = 0; i < MAX_SIZE; i++) {
            for (int j = 0; j < MAX_SIZE; j++) {
                gridmap[i][j] = '?'; //set it all to unknown
            }
        }
        gridmap[pos.y][pos.x] = Mark.HOME;
    }

    public LinkedList<Point> getNeighbours(Point in) {
        LinkedList<Point> out = new LinkedList<Point>();

        if (in.x+1 < MAX_SIZE) out.add(new Point(in.x+1,in.y));
        if (in.x-1 >= 0) out.add(new Point(in.x-1,in.y));

        if (in.y+1 < MAX_SIZE) out.add(new Point(in.x,in.y+1));
        if (in.y-1 >= 0) out.add(new Point(in.x,in.y-1));

        return out;
    }

    public char getPos(int y, int x) {
        return gridmap[y][x];
    }

    public char aheadObject(Point pos, int curOrient) {
        switch(curOrient) {
            case 0: return gridmap[pos.y-1][pos.x];
            case 1: return gridmap[pos.y][pos.x+1];
            case 2: return gridmap[pos.y+1][pos.x];
            case 3: return gridmap[pos.y][pos.x-1];
        }
        return '?';
    }

    public void appendGridMap(char[][] view, int curOrient, Point pos) {
        int x = pos.x;
        int y = pos.y;

        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                gridmap[y+i-2][x+j-2] = view[i][j];

                // update target position
                if (gridmap[y+i-2][x+j-2] == '$') {
                    treasurePos = new Point(x+j-2, y+i-2);
                }
            }
        }

        switch(curOrient) {
            case 0: gridmap[y][x] = '^'; break;
            case 1: gridmap[y][x] = '>'; break;
            case 2: gridmap[y][x] = 'v'; break;
            case 3: gridmap[y][x] = '<'; break;
        }

        gridmap[MAX_SIZE/2][MAX_SIZE/2] = Mark.HOME;
    }

    public Point getTreasurePos() {
        return treasurePos;
    }

    public void setTreasurePos(Point p) {
        treasurePos = p;
    }

    public boolean withinRange(Point p, char c[], int range) {
        for (int i = -range; i < range+1; i++) {
            for (int j = -range; j < range+1; j++) {
                for (int k = 0; k < c.length; k++) {
                    if (c[k] == gridmap[p.y+i][p.x+j]) {
                        return true;
                    }					
                }
            }
        }

        return false;
    }
};

public class Agent {

    public boolean hasAxe;
    public boolean hasKey;
    public boolean hasRaft;
    public boolean inBoat;
    public int numDynamite;
    public boolean hasTreasure;

    //0 = up, 1 = right, 2 = down, 3 = left
    public int curOrient; 
    public Point pos; 
    public LinkedList<Point> path;

    public MapGrid gmap;
    public AstarSearch astar;
    public BFSearch bfs;

    Agent() {
        numDynamite = 0;
        curOrient = 0;
        // start position
        pos = new Point(MapGrid.MAX_SIZE/2, MapGrid.MAX_SIZE/2); 
        path = new LinkedList<Point>();

        gmap = new MapGrid(pos);
        astar = new AstarSearch(gmap);
        bfs = new BFSearch(gmap);
    }

    public char[][] rightRotate(char[][] matrix) {
        int w = matrix.length;
        int h = matrix[0].length;
        char[][] ret = new char[h][w];
        for (int i = 0; i < h; ++i) {
            for (int j = 0; j < w; ++j) {
                ret[i][j] = matrix[w - j - 1][i];
            }
        }
        return ret;
    }

    public char[][] leftRotate(char[][] matrix) {
        int w = matrix.length;
        int h = matrix[0].length;   
        char[][] ret = new char[h][w];
        for (int i = 0; i < h; ++i) {
            for (int j = 0; j < w; ++j) {
                ret[i][j] = matrix[j][h - i - 1];
            }
        }
        return ret;
    }

    private void bfsSearch() {
        
        LinkedList<Character> obstacles = 
            new LinkedList<Character>(Arrays.asList('.', '~', '*', '-', 'T', '?'));

        if (hasAxe) obstacles.remove(new Character('T')); 
        if (hasKey) obstacles.remove(new Character('-')); 
        if (hasRaft) obstacles.remove(new Character('~'));

        boolean out;

        //go home if we have treasure
        if (hasTreasure) {
            out = getPathByBFS(new char[]{'H'}, obstacles, 0);
            if (out) {
                return;
            }
        }

        //try to go to treasure
        if (gmap.getTreasurePos() != null) {
            out = getPathByBFS(new char[]{'$'}, obstacles, 0);
            if (out) {
                return;
            }
        }
        obstacles.remove(new Character('?'));

        //look for items, then explore ?s you can reach
        out = getPathByBFS(new char[]{'a', 'd', 'k', '?'}, obstacles, 0);
        if (out) {
            return;
        }

        // look for ?2
        out = getPathByBFS(new char[]{'?'}, obstacles, 2);
        if (out) {
            return;
        }

        //look for far reaching ?s
        char array[] = {'?'};
        path = bfs.searchObject(pos, array, 2, obstacles);
        if (!path.isEmpty()) {
            return;
        }
    }

    private char astarSearch() {
        LinkedList<Character> obstacles = 
           new LinkedList<Character>(Arrays.asList('.', '~', '-', 'T', '?'));

        if (hasKey) obstacles.remove(new Character('-'));
        if (hasRaft) obstacles.remove(new Character('~'));

        char temp = getPathByAstar(new char[]{'$', 'a', 'd', 'k', '?'}, obstacles);

        if (temp != 0) {
            return temp;
        } else {
            // try boat
            if (!hasRaft) { // find Raft first
            	obstacles.remove(new Character('T'));
                temp = getPathByAstar(new char[]{'$','a','d','k','T','?'}, obstacles);
                if (temp != 0) {
                    return temp;
                }
            } else {
            	obstacles.remove(new Character('~'));
                temp = getPathByAstar(new char[]{'$','a','d','k','?'}, obstacles);
                if (temp != 0) {
                    return temp;
                }
            }
        }

        return 'X';
    }
    

	private boolean getPathByBFS(char targets[], LinkedList<Character> avoid, int offset) {
		LinkedList<Character> a = null;
		int waterIndex = 0;
		a = new LinkedList<Character>(avoid);
		
		LinkedList<Point> trail = bfs.searchObject(pos, targets, offset, a);
		waterIndex = getWaterPos(trail);
		if (trail.size() > 0) {
			Point p = trail.get(1);
			
			if (inBoat && waterIndex != 0) {
				if (gmap.getPos(p.y, p.x) == new Character(' ') 
						|| gmap.getPos(p.y, p.x) == new Character('T')) {
					if (hasPath(pos, trail.get(waterIndex))) {
						LinkedList<Character> av = new LinkedList<Character>(Arrays.asList('.', ' ', '*', 'T'));
						trail = bfs.searchPos(pos, trail.get(waterIndex), 0, av);
					}
				}
			}
			trail.removeFirst();
			path = trail;
			return true;
		}
				
		return false;
	}

    private char getPathByAstar(char targets[], 
            LinkedList<Character> walls) {

        LinkedList<Character> a = null;
        int waterStart = 0;

        for (int i = 0; i < targets.length; i++) {
            a = new LinkedList<Character>(walls);

            // path with out water
            LinkedList<Point> trailPath = 
                astar.aStarSearch(pos, targets[i], numDynamite, a);

            waterStart = getWaterPos(trailPath);

            if (trailPath.size() > 0) {
                Point p = trailPath.get(1);

                if (inBoat && waterStart != 0) {
                    if (gmap.getPos(p.y, p.x) == new Character(' ') 
                            || gmap.getPos(p.y,p.x) == new Character('T')) {
                        if (hasPath(pos, 
                                    trailPath.get(waterStart))) {
                            LinkedList<Character> av = 
                                new LinkedList<Character>(Arrays.asList('.', ' ', '*', 'T', '-'));
                            trailPath = bfs.searchPos(pos, trailPath.get(waterStart), 0, av);
                            p = trailPath.get(1);
                        }
                    }
                }

                if(getNextPoint().equals(p)) {
                    if (gmap.getPos(p.y, p.x) == '*'){
                        return 'b';
                    }
                    return 'f';
                } else {
                    return 'l';
                }
            }
        }

        return 0;
    }

    private int getWaterPos(LinkedList<Point> trailPath) {
        for (int i = 1; i < trailPath.size(); i++) {
            Point p = trailPath.get(i);
            if (gmap.getPos(p.y, p.x) == '~') {
                return i;
            }	
        }
        return 0;
    }

    private Point findRaft(Point waterTile) {
        LinkedList<Character> walls = 
            new LinkedList<Character>(Arrays.asList('.', ' ', '*'));
        char array[] = {'T'};
        LinkedList<Point> tempPath = bfs.searchObject(waterTile, array, 0, walls);
        Point p = null;
        if (tempPath.size() > 0) {
            p = tempPath.getLast();
        }
        return p;

    }

    private boolean hasPath(Point a, Point b) {
        LinkedList<Character> walls 
            = new LinkedList<Character>(Arrays.asList('.', ' ', '*', '-', 'T'));
        LinkedList<Point> tempPath = bfs.searchPos(a, b, 0, walls);

        if (tempPath.size() > 0) {
            return true;
        }

        return false;
    }

    private Point getNextPoint() {
        switch(curOrient) {
            case 0: return new Point(pos.x, pos.y-1);
            case 1: return new Point(pos.x+1, pos.y);
            case 2: return new Point(pos.x, pos.y+1);
            case 3: return new Point(pos.x-1, pos.y);
        }
        return null;
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

    public char get_action(char view[][]) {
		try {
			Thread.sleep(50);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

        switch(curOrient) { // change view of map
            case 1: 
                view = rightRotate(view); break;
            case 2: 
                view = leftRotate(view); 
                view = leftRotate(view); break;
            case 3: 
                view = leftRotate(view); break;
        }

        gmap.appendGridMap(view, curOrient, pos);

        char c = 'l';

        if (path.size() > 0) {
            Point p = path.getFirst();
            if (getNextPoint().equals(p)) {
                c = 'f';
                path.removeFirst();
            } else {
                c = 'l';
            }
        } else {
            bfsSearch();
            if (path.size() > 0) {
                Point p = path.getFirst();
                if (getNextPoint().equals(p)) {
                    c = 'f';
                    path.removeFirst();
                } else {
                    c = 'l';
                }
            } else {
                c = astarSearch();
            }
            path.clear();
        }

        char in = gmap.aheadObject(pos, curOrient);

        if (in == 'T' && hasAxe == true) {
            c = 'c';
            hasRaft = true;
        }

        if (in == '-' && hasKey == true) {
            c = 'u';
        }

        // do update after each action
		switch (c) {
		case 'l':
			curOrient--;
			break;
		case 'r':
			curOrient++;
			break;
		case 'f':
			if (in == 'T' || in == '*') {
				c = astarSearch();
				break;
			}
			if (in == '~' && !hasRaft) {
				break;
			}
			if (in == '$') {
				hasTreasure = true;
				gmap.setTreasurePos(null);
			}
			if (in == 'a')
				hasAxe = true;
			if (in == 'k')
				hasKey = true;
			if (in == 'd')
				numDynamite++;
			if (in == '~')
				inBoat = true;
			if (in == ' ' && inBoat) {
				inBoat = false;
				hasRaft = false;
			}

			switch (curOrient) {
			case 0:
				pos.y--;
				break;
			case 1:
				pos.x++;
				break;
			case 2:
				pos.y++;
				break;
			case 3:
				pos.x--;
				break;
			}
			break;
		case 'b':
			numDynamite--;
			break;
		}

        if (curOrient < 0) curOrient = 3;
        if (curOrient > 3) curOrient = 0;


        if (numDynamite < 0) {
            System.exit(1);
        }

        return c;
    }


    //please don't touch below
    public static void main(String[] args) {
        InputStream in = null;
        OutputStream out = null;
        Socket socket = null;
        Agent agent = new Agent();
        char view[][] = new char[5][5];
        char action = 'F';
        int port;
        int ch;
        int i, j;
        long time = System.currentTimeMillis();

        if (args.length < 2) {
            System.out.println("Usage: java Agent -p <port>\n");
            System.exit(-1);
        }

        port = Integer.parseInt(args[1]);

        try { // open socket to Game Engine
            socket = new Socket("localhost", port);
            in = socket.getInputStream();
            out = socket.getOutputStream();
        } catch (IOException e) {
            System.out.println("Could not bind to port: " + port);
            System.exit(-1);
        }

        try { // scan 5-by-5 wintow around current location
            while (true) {
                for (i = 0; i < 5; i++) {
                    for (j = 0; j < 5; j++) {
                        if (!((i == 2) && (j == 2))) {
                            ch = in.read();
                            if (ch == -1) {
                                System.exit(-1);
                            }
                            view[i][j] = (char) ch;
                        }
                    }
                }
                //agent.print_view( view ); // COMMENT THIS OUT BEFORE SUBMISSION
                action = agent.get_action(view);
                out.write(action);
            }
        } catch (IOException e) {
            System.out.println("Lost connection to port: " + port);
            System.exit(-1);
        } finally {
            try {
                socket.close();
            } catch (IOException e) {
            }
        }
    }
} 
