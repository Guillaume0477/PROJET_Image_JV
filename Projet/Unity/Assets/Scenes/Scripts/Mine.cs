using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Mine : MonoBehaviour
{   
    public Light light;

    private bool exploded = false;
    private float ennemyDammage = 80;
    private float manaNeeded = 30;
    private bool lighting = false;
    private float time_blinking = 0.3f;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if(lighting)
        {
            StartCoroutine("BlinkingHigh");
        }
        else
        {
            StartCoroutine("BlinkingDown");
        }

        if (transform.GetChild(1).gameObject.activeSelf)
        {
            if(transform.GetChild(1).gameObject.transform.localScale.x >= 7){
                Destroy(gameObject);
            } 
            else {
                transform.GetChild(1).gameObject.transform.localScale += new Vector3(0.2f, 0.2f, 0.2f);
                ennemyDammage -= 80.0f/(7.0f*5.0f);
            }
        }

        if (exploded){
            transform.GetChild(0).gameObject.SetActive(false);
            transform.GetChild(1).gameObject.SetActive(true);
        }
    }

    IEnumerator BlinkingHigh()
    {
        light.gameObject.SetActive(true);
        yield return new WaitForSeconds(time_blinking);
        lighting = false;
    }

    IEnumerator BlinkingDown()
    {
        light.gameObject.SetActive(false);
        yield return new WaitForSeconds(time_blinking);
        lighting = true;
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