#include <bits/stdc++.h>
using namespace std;

//変更テスト

// 表、裏、上、左、右、下の順
// 展開図

    //      18,19,20

    // 21   0 ,1 ,2   24 
    // 22   3, 4, 5   25
    // 23   6, 7, 8   26

    //      27,28,29

    //      15,16,17
    //      12,13,14
    //      9 ,10,11



string TurnUp(string ColorPattern){
    swap(ColorPattern[0], ColorPattern[11]);
    swap(ColorPattern[1], ColorPattern[10]);
    swap(ColorPattern[2], ColorPattern[9]);
    swap(ColorPattern[21], ColorPattern[24]);
    swap(ColorPattern[18], ColorPattern[20]);
    return ColorPattern;
}

string TurnLeft(string ColorPattern){
    swap(ColorPattern[0], ColorPattern[15]);
    swap(ColorPattern[3], ColorPattern[12]);
    swap(ColorPattern[6], ColorPattern[9]);
    swap(ColorPattern[21], ColorPattern[23]);
    swap(ColorPattern[18], ColorPattern[27]);
    return ColorPattern;
}

string TurnRight(string ColorPattern){
    swap(ColorPattern[2], ColorPattern[17]);
    swap(ColorPattern[5], ColorPattern[14]);
    swap(ColorPattern[8], ColorPattern[11]);
    swap(ColorPattern[24], ColorPattern[26]);
    swap(ColorPattern[20], ColorPattern[29]);
    return ColorPattern;
}

string TurnDown(string ColorPattern){
    swap(ColorPattern[6], ColorPattern[17]);
    swap(ColorPattern[7], ColorPattern[16]);
    swap(ColorPattern[8], ColorPattern[15]);
    swap(ColorPattern[23], ColorPattern[26]);
    swap(ColorPattern[27], ColorPattern[29]);
    return ColorPattern;
}


string InitialPattern = "WWWWWWWWWYYYYYYYYYRRRBBBGGGOOO";
map<string,int> mp;



void Init(){
    mp[InitialPattern] = 0;
    queue<string> que;
    que.push(InitialPattern);
    while(!que.empty()){
        string OldPattern = que.front();
        que.pop();
        string up = TurnUp(OldPattern);
        string right = TurnRight(OldPattern);
        string left = TurnLeft(OldPattern);
        string down = TurnDown(OldPattern);
        if(!mp.count(up)){
            que.push(up);
            mp[up] = mp[OldPattern] + 1;
        }

        if(!mp.count(right)){
            que.push(right);
            mp[right] = mp[OldPattern] + 1;
        }
        if(!mp.count(left)){
            que.push(left);
            mp[left] = mp[OldPattern] + 1;
        }
        if(!mp.count(down)){
            que.push(down);
            mp[down] = mp[OldPattern] + 1;
        }
    }
}

void Solve(string InputPattern){
    while(1){
        if(!mp.count(InputPattern)){
            cout << "Invalid input" << endl;
            break;
        }
        if(InputPattern == InitialPattern){
            cout << "Solved" << endl;
            break;
        }
        if(mp[InputPattern] > mp[TurnUp(InputPattern)]){
            InputPattern = TurnUp(InputPattern);
            cout << "TurnUp " << InputPattern << endl;
        }
        else if(mp[InputPattern] > mp[TurnRight(InputPattern)]){
            InputPattern = TurnRight(InputPattern);
            cout << "TurnRight " << InputPattern << endl;
        }
        else if(mp[InputPattern] > mp[TurnLeft(InputPattern)]){
            InputPattern = TurnLeft(InputPattern);
            cout << "TurnLeft " << InputPattern << endl;
        }
        else if(mp[InputPattern] > mp[TurnDown(InputPattern)]){
            InputPattern = TurnDown(InputPattern);
            cout << "TurnDown " << InputPattern << endl;
        }
        else{
            cout << "ERROR" << endl;
        }
    }
}

int main(){
    Init();
    string Input;
    cin>>Input;
    Solve(Input);
    return 0;
}
