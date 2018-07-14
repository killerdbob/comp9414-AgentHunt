
import java.util.*;
import java.awt.Point;

public class AstarSearch {
    public MapGrid gdmap;

    public AstarSearch(MapGrid mg) {
        gdmap = mg;
    }

    public LinkedList<Point> aStarSearch(Point from, char to, 
            int maxDys, LinkedList<Character> walls) {

        Queue<CostState> openSet = new PriorityQueue<CostState>(1,
                new Comparator<CostState>() {

            @Override
            public int compare(CostState cost1, CostState cost2) {
                return cost1.getCost() - cost2.getCost();
            }
        });

        ArrayList<CostState> closedSet = new ArrayList<CostState>();
        LinkedList<Point> trailPath = new LinkedList<Point>();
        HashMap<Point, Point> backtrackMap = new HashMap<Point, Point>();

        CostState first = new CostState(from, 0);
        openSet.add(first);

        while (!openSet.isEmpty()) {
            CostState current = new CostState(new Point(0, 0), 0);
            current.setNode(openSet.peek().getNode());
            current.setCost(openSet.peek().getCost());
            openSet.remove();

            closedSet.add(current);

            char array[] = {to};
            // found it
            if (gdmap.withinRange(current.getNode(), array, 0)) {
                trailPath.add(current.getNode());
                while (!current.getNode().equals(from)) {
                    trailPath.addFirst(backtrackMap.get(current.getNode()));
                    current.setNode(backtrackMap.get(current.getNode()));
                }
                break;
            }

            for (Point p : gdmap.getNeighbours(current.getNode())) {
                if (walls.contains(gdmap.getPos(p.y, p.x))) {
                    continue;
                }

                CostState temp = new CostState(p, current.getCost());
                // walls
                if (gdmap.getPos(p.y, p.x) == '*') {
                    temp.setCost(current.getCost() + 100);
                }

                // land or water
                if (gdmap.getPos(p.y, p.x) == ' ' 
                        || gdmap.getPos(p.y, p.x) == '~') {
                    temp.setCost(current.getCost() + 1);
                }

                if (checkClosedSet(closedSet, temp.getNode()) == false 
                        && checkOpenSet(openSet, temp.getNode(), 
                            temp.getCost()) == false) {
                    if (!backtrackMap.containsKey(p)) {
                        openSet.add(temp);
                        backtrackMap.put(p, current.getNode());
                    }
                }
            }
        }

        int bombsNeeded = 0;

        for (int j = 0; j < trailPath.size(); j++) {
            if (gdmap.getPos(trailPath.get(j).y, trailPath.get(j).x) == '*') {
                bombsNeeded++;
            }
            if (bombsNeeded > maxDys) {
                trailPath.clear();
            }
        }

        return trailPath;
    }

    /**
     * @param set the open set
     * @param name target point
     * @param cost cost of the path
     * @return true if found, false otherwise
     */
    private boolean checkOpenSet(Queue<CostState> set, Point name, 
            int cost) 
    {
        ArrayList<CostState> list = new ArrayList<CostState>();
        CostState temp = new CostState(new Point(0, 0), 0);
        int i = 0;

        while (!set.isEmpty()) {
            list.add(set.remove());
        }
        set.addAll(list);

        for(i = 0; i < list.size(); i++) {
            temp = list.get(i);

            if(temp.getNode().x == name.x 
                    && temp.getNode().y == name.y 
                    && temp.getCost() > cost) {
                set.remove(temp);
                temp.setCost(cost);
                set.add(temp);

                return true;
            }
        }

        return false;
    }

    /**
     * @param set the closed set
     * @param name target point
     * @return true for found, false otherwise
     */
    private boolean checkClosedSet(ArrayList<CostState> set, Point name) 
    {
        int i = 0;

        for (i = 0; i < set.size(); i++) {
            if (set.get(i).getNode().x == name.x 
                    && set.get(i).getNode().y == name.y) {
                return true;
            }
        }
        return false;
    }

    class CostState {

        public CostState(Point newNode, int cost) {
            node = newNode;
            g = cost;
        }

        public Point getNode() {
            return node;
        }

        public int getCost() {
            return g;
        }

        public void setNode(Point newVal) {
            node = newVal;
        }

        public void setCost(int newVal) {
            g = newVal;
        }

        private Point node;
        private int g;
    }

}
