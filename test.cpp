#include <iostream>
#include <fstream>
using namespace std;
int main(){
    ifstream input;
    input.open("input.txt");
    int n=33131;
    int kq=1,res=1;
    int a[n];
    for (int i=1;i<n;i++)
        input>>a[i];
    int vt=0;
    for (int i=0;i<n;i++)
        if (a[i]==1)
            kq++;
        else{
            if (res<kq){
                res=kq;
                vt=i;
            }
            kq=1;
        }
    cout<<res<<" "<<vt<<endl;
    cout<<"----";
}