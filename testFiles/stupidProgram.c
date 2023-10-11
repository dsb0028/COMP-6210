int main() {
    int a = 4;
    int b = 2;
    int c = 8;
    int d = 9; 
    if (a > 2 || (b < 3 && c > 2) || (a<=2 && b>2)) {
        a = 6;
        if(b<10) {
            b = 4;
        }
        else {
            if(d<20) {
                b = 128;
             }
        }
    } 
/*
    int c = 20;
    if(a<=2 && b>2) {
        a = 6;
    }
    else {
        if(b<10) {
            b = 4;
        }
    }
*/
    return 0; 
}