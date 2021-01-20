using UnityEngine;
// Include the namespace required to use Unity UI
using UnityEngine.UI;
using System.Collections;
using UnityEngine.SceneManagement;

public class MonsterGeneratorTutorial : MonoBehaviour {
    public GameObject ennemy_prefab;
    public PlayerStatsTutorial playerStats;
    public PlayerControllerTutorial player;

    private bool isSpawned;

    void Start()
    {
        EnnemyAITutorial EAI = ennemy_prefab.GetComponent<EnnemyAITutorial>();
		EAI.Target = playerStats;
    }

    void Update(){
        if(!isSpawned)
        {
            MonsterGeneration();
        }
    }

    void MonsterGeneration()
    {
        if(player.fight_text.enabled == true)
        {
            isSpawned = true;
            Instantiate(ennemy_prefab, transform.position, Quaternion.identity);
        }
    }
}