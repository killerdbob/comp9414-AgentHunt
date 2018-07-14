import java.util.*;
import java.awt.Point;

public class BFSearch {
    public MapGrid gmap;

    public BFSearch(MapGrid mg) {
        gmap = mg;
    }

    public LinkedList<Point> searchObject(Point start, char in[], 
            int offset, LinkedList<Character> walls) 
    {

        LinkedList<Point> Q = new LinkedList<Point>();
        HashMap<Point, Point> backtrackMap = new HashMap<Point, Point>();

        Point v = null;
        boolean foundTarget = false;

        Q.add(start); //enqueue
        while (!Q.isEmpty()) {
            v = Q.poll(); //dequeue

            //process v
            if (gmap.withinRange(v, in, offset)) {
                foundTarget = true;
                break;
            }

            for (Point p : gmap.getNeighbours(v)) {
                if (walls.contains(gmap.getPos(p.y, p.x))) {
                    continue;
                }

                if (!backtrackMap.containsKey(p)) {
                    Q.add(p);
                    backtrackMap.put(p, v);
                }
            }
        }

        if (!foundTarget) {
            return new LinkedList<Point>();
        }

        LinkedList<Point> trailPath = new LinkedList<Point>();
        trailPath.add(v);

        while(!v.equals(start)) {
            trailPath.addFirst(backtrackMap.get(v));
            v = backtrackMap.get(v);
        }

        return trailPath;
    }


    public LinkedList<Point> searchPos(Point start, Point end, 
            int offset, LinkedList<Character> walls) 
    {

        LinkedList<Point> Q = new LinkedList<Point>();
        HashMap<Point, Point> backtrackMap = new HashMap<Point, Point>();

        Point v = null;
        boolean foundTarget = false;

        Q.add(start); //enqueue
        while (!Q.isEmpty()) {
            v = Q.poll(); //dequeue

            if (v.x == end.x && v.y == end.y) {
                foundTarget = true;
                break;
            }

            for (Point p : gmap.getNeighbours(v)) {
                if (walls.contains(gmap.getPos(p.y, p.x))) {
                    continue;
                }

                if (!backtrackMap.containsKey(p)) {
                    Q.add(p);
                    backtrackMap.put(p, v);
                }
            }
        }

        if (!foundTarget) { // no found
            return new LinkedList<Point>();
        }

        LinkedList<Point> trailPath = new LinkedList<Point>();
        trailPath.add(v);

        while(!v.equals(start)) {
            trailPath.addFirst(backtrackMap.get(v));
            v = backtrackMap.get(v);
        }

        return trailPath;
    }

}
