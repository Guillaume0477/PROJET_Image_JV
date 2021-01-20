using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CountEnnemyKilled : MonoBehaviour
{
    private int ennemyKilled = 0;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void oneMore()
    {
        ennemyKilled += 1;
        GetComponent<Text>().text = ennemyKilled.ToString();
    }

    public int getEnnemyKilled()
    {
        return ennemyKilled;
    }

}
