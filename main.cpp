#include <bits/stdc++.h>
#include "lib/HashMap.hpp"
using namespace std;
using namespace hashmap;

int main() {
    HashMap<string, int> mp(100), mp2(200);
    vector<string> keys{"HI", "ID", "PP", "DD"};
    for(int i = 0; i < keys.size(); ++i)
        mp[keys[i]] = i;
    mp["HI"] = 100;
    for(const auto& p : mp)
        cout << p.first << ' ' << p.second << '\n';
}