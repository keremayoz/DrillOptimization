/*********************************************
 * OPL 12.9.0.0 Model
 * Author: ATTJ
 * Creation Date: Dec 26, 2019 at 11:46:25 PM
 *********************************************/

// problem size
int n = ...;
range nodes = 1..n;

// edge tuple
tuple edge {
	int i;
	int j;
}

setof(edge) edges = {<i,j> | i,j in nodes : i!= j};
float dist[edges] = ...;
setof(edge) blocked = ...;

// decision variable
dvar boolean x[edges];
dvar float+ u[1..n];

// expressions
dexpr float TotalDistance = sum(e in edges) dist[e]*x[e];

// objective
minimize TotalDistance;

// constraints
subject to {
	
	forall (j in nodes)
		flow_in:
		sum( i in nodes: i != j) x[<i,j>] == 1;
	
	forall (i in nodes)
		flow_out:
		sum( j in nodes: j != i) x[<i,j>] == 1;
	
	forall (e in blocked)
	  	no_path:
	  	x[e] == 0;
	  
	 u[1] == 1; 
	 forall(i in 2..n) 2<=u[i]<=n;
	 forall(e in edges: e.i!=1 && e.j!=1) (u[e.j]-u[e.i])+1<=(n-1)*(1-x[e]);
}

execute {
  var ofile = new IloOplOutputFile("result.txt");
  var v;
  for( v in x) {
  	ofile.write(x[v]);
  	ofile.write(',');
  }  
}  