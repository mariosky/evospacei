int[] chromosome = 
{ 
  2,   2,   2,  2,  2,  2,
  2,   11,  11, 2, 2,  2,
  2,   2,   2,  2,  2,  2,
  2,   2,   0,  11, 2,  2,
  2,   2,   0,  11, 2,  2,
  2,   2,   2,  2,  2,  2,
  2,   2,   2,  2,  2,  2,
  2,   2,   2,  2,  2,  2, 
  2,   2,   2,  2,  2,  2,
  2,   2,   2,  2,  2,  2,
  2,   2,   2,  2,  2,  2 
};

Color[] pallete = new Color[12];

int CANVAS_SIZE = 200;
int ROWS = 5;

ArrayList trian;

int[] getChromosome() { return chromosome; }
ArrayList getPoints() { return trian; }

void setup()
{
 size(CANVAS_SIZE,CANVAS_SIZE);
 trian = new ArrayList(); 

 
 //frameRate(1);
 noLoop();
 pallete[0] = new Color(#333333); //Gris Oscuro
 pallete[1] = new Color(#7B2B83); //Purple
 pallete[2] = new Color(#CCCCCC); //Gris Claro
 pallete[3] = new Color(#AEDD3C); //Verde
 
 pallete[4] = new Color(#00A7E5); // Azul Cielo
 pallete[5] = new Color(#E4D5ED); // Purple Claro
 pallete[6] = new Color(#777777); // Gris Oscuro
 pallete[7] = new Color(#A7005B); // Rojo
 
 pallete[8] = new Color(#000000); //Gris Oscuro !!!
 pallete[9] = new Color(#F89829); // Naranjita
 pallete[10] = new Color(#B31E6D); // Rosa Claro
 pallete[11] = new Color(#FFFFFF); // Blanco !!!
 
 background(pallete[2].hex); 
 
 //   
 // Base y altura para hacer el grid 
 //
 
 int lado = 32;
 int mitad = lado/2;
 int altura = int ( pow( pow( lado,2) - pow( lado/2,2), 0.5));
 int xorigen = (CANVAS_SIZE-(altura*6)) / 2;
 int yorigen = ((CANVAS_SIZE-(altura*7)) / 2 )+mitad;
 
 

 int c = 0;
 
 for (int j = 0; j<ROWS; j++ )
 {
   
   for (int i = 0; i<3;i++)
   {
   trian.add(new Tri(xorigen + (altura*2*i),           yorigen,  
                                               xorigen + altura + (altura*2*i),  yorigen - mitad, 
                                               xorigen + altura + (altura*2*i),  yorigen + mitad));
                                               
   trian.add(new Tri(xorigen + (altura*2*(i+1))     ,  yorigen, 
                                               xorigen + altura + (altura*2*i), yorigen - mitad, 
                                               xorigen + altura + (altura*2*i), yorigen +mitad));
   }
   
   for (int i = 0; i<3;i++)
    {
   trian.add(new Tri( xorigen + (altura*2*i),           yorigen, 
                                               xorigen + altura + (altura*2*i),  yorigen + mitad, 
                                               xorigen + (altura*2*i),           yorigen + lado
                                               ));
                                               
   trian.add(new Tri( xorigen + altura + (altura*2*(i)) ,  yorigen +mitad ,
                                               xorigen + (altura*2*(i+1))     ,  yorigen, 
                                               xorigen + (altura*2*(i+1))     ,  yorigen + lado 
                                              ));
   }
 
   yorigen += lado;
 }
 
 for (int i = 0; i<3;i++)
  {
   trian.add( new Tri( xorigen + (altura*2*i),           yorigen,  
                                               xorigen + altura + (altura*2*i),  yorigen - mitad, 
                                               xorigen + altura + (altura*2*i),  yorigen + mitad));

 
  trian.add( new Tri(xorigen + (altura*2*(i+1))     ,  yorigen, 
                                               xorigen + altura + (altura*2*i), yorigen - mitad, 
                                               xorigen + altura + (altura*2*i), yorigen +mitad));

  }

 
 
  
 //  noStroke(); 
// for (int j= 0; j< trian.size(); j++)
// {
//   ( (Tri) trian.get(j)).display();
// }
  
 //save("line4.tif");
}

void draw()
{
 for (int j= 0; j< trian.size(); j++)
 {
     ( (Tri) trian.get(j)).display(pallete[chromosome[j]]);
 }

}

void paint()
{
 for (int j= 0; j< trian.size(); j++)
 {
     ( (Tri) trian.get(j)).display(pallete[chromosome[j]]);
 }

}

class Tri
{
  int x1,y1,x2,y2,x3,y3;
  

Tri( int x1, int y1,int x2, int y2,int x3, int y3  )
{
 this.x1 = x1;
 this.y1 = y1;
 this.x2 = x2;
 this.y2 = y2;
 this.x3 = x3;
 this.y3 = y3;
}
 void display(Color f)
 { 
   //stroke(1); 
    noStroke();
     // int [] alpha = {0,127,192,192,225,255,255}  ;
     // int [] alpha = {0,0,0,0,0,255}  ;
    
   //  fill(f.hex, alpha[int(random(6) ) ]);
   //  fill(fill.hex, alpha[int(random(6) ) ]);
   fill(f.hex);
  //fill(pallete[int(random(11))].hex);
   
   //smooth();
   triangle(x1, y1,x2, y2,x3,y3);
  
}

}


class Color
{
  int R;
  int G;
  int B;
  int hex;
  Color( int r, int g, int b)
  {
    R=r; G=g; B=b;
  }
  
 Color(int hex)
 {
  
  this.hex = hex;
  
  
 } 
}



