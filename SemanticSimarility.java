
import de.linguatools.disco.CorruptConfigFileException;
import de.linguatools.disco.DISCO;
import de.linguatools.disco.DISCO.SimilarityMeasure;
import de.linguatools.disco.WrongWordspaceTypeException;

import java.io.FileNotFoundException;
import java.io.IOException;

public class SemanticSimarility  {
    
	public static void main(String[] args) throws IOException, WrongWordspaceTypeException{

        // path to the DISCO word space directory
        String discoDir = args[0];
        // second argument is the input word
        String firstWord = args[1];
        
        String secondWord = args[1];
        
        // create instance of class DISCO.      *
	    DISCO disco;
        try {
            disco = new DISCO(discoDir, false);
        } catch (FileNotFoundException | CorruptConfigFileException ex) {
            System.out.println("Error creating DISCO instance: "+ex);
            return;
        }

       
        // retrieve the most similar words for the input word
        try {
        	StringBuilder builder = new StringBuilder();
        	
        	float similarityScore = disco.semanticSimilarity(firstWord, secondWord, SimilarityMeasure.COSINE);
        	
        	builder.append("Semantic Similarity between ");
        	builder.append(firstWord);
        	builder.append(" ");
        	builder.append(secondWord);
        	builder.append(" = ");
        	builder.append(similarityScore);
        	
            System.out.println(builder.toString());
        } catch (Exception ex) {
            System.out.println("Error retrieving the word: "+ex);
            return;
        }    }
}
