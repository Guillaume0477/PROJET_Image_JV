using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MineTutorial : MonoBehaviour
{   
    private bool exploded = false;
    private float ennemyDammage = 80;
    private float manaNeeded = 0;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (transform.GetChild(1).gameObject.activeSelf){
            if(transform.GetChild(1).gameObject.transform.localScale.x >= 7){
                Destroy(gameObject);
            } 
            else {
                transform.GetChild(1).gameObject.transform.localScale += new Vector3(0.2f, 0.2f, 0.2f);
                ennemyDammage -= 0;//80.0f/(7.0f*5.0f);
            }
        }

        if (exploded){
            transform.GetChild(0).gameObject.SetActive(false);
            transform.GetChild(1).gameObject.SetActive(true);
        }
    }

    public float getEnnemyDamage(){
        return ennemyDammage;
    }

    public float getManaNeeded(){
        return manaNeeded;
    }

    public void Explosion(){
        exploded = true;
    }

}