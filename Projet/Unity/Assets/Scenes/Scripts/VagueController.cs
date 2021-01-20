using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class VagueController : MonoBehaviour
{
    public CountEnnemyKilled count;

    private float repop_time = 30.0f;
    public bool play = true;
    private int currVague = 1;

    private bool newVague = false;

    // Start is called before the first frame update
    void Start()
    {
        GetComponent<Text>().text = currVague.ToString();
    }

    // Update is called once per frame
    void Update()
    {
        if ((count.getEnnemyKilled()%24 == 0) && (newVague))
        {
            StartCoroutine("NewVague");
        } 
        else if (count.getEnnemyKilled()%24 == 1)
        {
            newVague = true;
        }
    }

    IEnumerator NewVague(){
        play = false;
        newVague = false;
        yield return new WaitForSeconds(5.0f);
        currVague += 1;
        if (repop_time == 10.0f)
        {
            repop_time = 30.0f;
        } 
        else 
        {
            repop_time -= 10.0f;
        }

        GetComponent<Text>().text = currVague.ToString();

        play = true;
    }

    public int getCurrVague()
    {
        return currVague;
    }

    public float getRepopTime()
    {
        return repop_time;
    }
}
