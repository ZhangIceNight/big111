
public class App_woff {

  private Woff1Font woffFont = new Woff1Font();
  private int segCount = 0;
  private int[] endCount = null;
  private int[] startCount = null;
  private int[] isDealte = null;
  private int[] idRangeOffset = null;
  private int[] locaOffset = null;
  private String[] MD5s = null;


  public static void main(String[] args) {

    File dir = new File("E:/58/st/简历/");
    if(dir.isDirectory()) {
      File[] files = dir.listFiles();
      for(File f : files) {
        String name = f.getName();
        if(!name.endsWith("html")){
          continue;
        }
        if(name.endsWith("64.html")){
          continue;
        }
        System.out.println(name);
        try {

          App_woff app = new App_woff();
          app.loadMappingFile("E:/word2md5");
          String page = IReader.cat(f.getAbsolutePath());
          if(page.length() < 20000){
            continue;
          }
          String infoPart = app.getInfoPart(page);
          String textBase64 = IMatch.findOne(page, "woff;charset=utf-8;base64,(.*?)[)]  format").trim();
          List<String> longHtmlWords = app.getLongHtmlWords(infoPart);
          List<Integer> intHtmlWord = app.longHtmlWords2Int(longHtmlWords);

//          System.print.println(textBase64);

          app.solve(textBase64, intHtmlWord);
        }catch (Exception e){

          e.printStackTrace();
          System.exit(0);
        }
      }
    }
  }


  private String getInfoPart(String originPage) {
    try {
      String info = IMatch.findOne(originPage, "<div class=\"base-info\">([\\s\\S]*?)\r\n\t</div>");

      if(info == null){
        System.out.println(originPage);
        System.exit(0);
      }

      return info.trim();
//      System.print.println(info);
//      List<Integer> htmlWordValue = new ArrayList<>();

    } catch (Exception e) {
      e.printStackTrace();
    }
    return null;
  }

  public List<String> getLongHtmlWords(String infoPart){
    return IMatch.find(infoPart, "([&]#x[0-9a-f]{4};)");
  }

  public List<Integer> longHtmlWords2Int(List<String> ls){
    List<Integer> result = new ArrayList<>();
    for(String s : ls){
      result.add(longHtmlword2Value(s));
    }
    return result;
  }

  private int hex2int(char c) {
    if ((c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F')) {
      return c - 'a' + 10;
    }
    if(c >= '0' && c <= '9'){
      return c - '0';
    }
    return -1;
  }

  public int hex2int(String str) {
    int sum = 0;
    for (int i = 0; i < str.length(); i++) {
      char c = str.charAt(i);
      sum = sum * 16;
      sum += hex2int(c);
    }
    return sum;
  }

  // &#xe5e7;
  private int longHtmlword2Value(String htmlWord) {
    if(htmlWord != null && htmlWord.length() == 8){
      return hex2int(htmlWord.substring(3, 7));
    }
    return -1;
  }

  public static Map<String, String> MD52WORD = new HashMap<>();

  public void loadMappingFile(String fileName) {
    try {
      IReader reader = new IReader(fileName);
      String line = "";
      while ((line = reader.readLine()) != null) {
        String[] strs = line.split("\t");
        MD52WORD.put(strs[1], strs[0]);
      }
    } catch (Exception e) {
      e.printStackTrace();
    }
  }


  // 返回网页中的字符(int)，对应的文本字符
  public Map<Integer, String> solve(String textBASE64, List<Integer> htmlWordValues) {
    try {
      byte[] fontData = Base64.decodeBase64(textBASE64);

//      IOUtils.write(fontData, new FileWriter("E:/ssss.woff"));
      WoffParser woffParser = new WoffParser();
      woffParser.parse(fontData, woffFont);

//      System.print.println(woffFont.getFonts().size());
//
      List<WoffTable> ls = woffFont.getTables();
//      for (WoffTable wt : ls) {
//        System.print.println(
//            wt.getTag() + "\t" + wt.origLength() + "\t" + wt.getTableData().length + "\t" + wt
//                .getCompressedData().length);
//      }
      // 处理映射
      for (WoffTable wt : ls) {
        if (wt.getTag().equals("cmap")) {
          parseCMAP(wt.getTableData());
        }
      }

      for (WoffTable wt : ls) {
        if (wt.getTag().equals("loca")) {
          parseLOCA(wt.getTableData());
        }
      }
      for (WoffTable wt : ls) {
        if (wt.getTag().equals("glyf")) {
          parseGLYF(wt.getTableData());
        }
      }

      Map<Integer, String> htmlWordValue2Symbol = new HashMap<>();

      for(int v : htmlWordValues){
        String md5 = getMD5(v);
//        System.print.println(">>>>>");
        if(MD52WORD.containsKey(md5)){
          htmlWordValue2Symbol.put(v, MD52WORD.get(md5));
//          System.print.println(MD52WORD.get(md5));
        }else{
//          System.print.println(v);
          System.out.println("------------");
//          System.exit(0);
        }
      }

      return htmlWordValue2Symbol;


    } catch (Exception e) {
      e.printStackTrace();
    }
    return null;
  }


  public void solve(String textBASE64, Map<String, Integer> htmlMapping) {
    try {
      byte[] fontData = Base64.decodeBase64(textBASE64);

//      IOUtils.write(fontData, new FileWriter("E:/ssss.woff"));
      WoffParser woffParser = new WoffParser();
      woffParser.parse(fontData, woffFont);

//      System.print.println(woffFont.getFonts().size());
//
      List<WoffTable> ls = woffFont.getTables();
//      for (WoffTable wt : ls) {
//        System.print.println(
//            wt.getTag() + "\t" + wt.origLength() + "\t" + wt.getTableData().length + "\t" + wt
//                .getCompressedData().length);
//      }
      // 处理映射
      for (WoffTable wt : ls) {
        if (wt.getTag().equals("cmap")) {
          parseCMAP(wt.getTableData());
        }
      }

      for (WoffTable wt : ls) {
        if (wt.getTag().equals("loca")) {
          parseLOCA(wt.getTableData());
        }
      }
      for (WoffTable wt : ls) {
        if (wt.getTag().equals("glyf")) {
          parseGLYF(wt.getTableData());
        }
      }

      IWriter writer = new IWriter("E:/word2md5", true);

      System.out.println("segCount = " + segCount);

      for (Map.Entry<String, Integer> entry : htmlMapping.entrySet()) {
        System.out.println(
            entry.getKey() + "\t" + getGlyphId(entry.getValue()) + "\t" + getMD5(entry.getValue()));
        writer.writeln(entry.getKey() + "\t" + getMD5(entry.getValue()));
      }

      writer.close();
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  public void save(String outFile) {

  }

  public void solve() {
    App_woff app = new App_woff();
    byte[] fontData = app.loadBASE64("E:/base64.txt");
  }

  public void parseGLYF(byte[] data) {
    try {
      MD5s = new String[segCount];
      for (int i = 0; i < segCount; i++) {
        int start = locaOffset[i] * 2;
        int numberOfContours = toInt(sub(data, start, start + 1));
        int xMin = toShort(sub(data, start + 2, start + 3));
        int yMin = toShort(sub(data, start + 4, start + 5));
        int xMax = toShort(sub(data, start + 6, start + 7));
        int yMax = toShort(sub(data, start + 8, start + 9));

        String s = numberOfContours + "," + xMin + "," + yMin + "," + xMax + "," + yMax;
        String md5 = StringUtils.MD5(s);

//        System.print.println("-----------" + start + "\t" + numberOfContours + "-----------");
////        System.print.println("\t\t"+start);
////        System.print.println("\t\tnumberOfContours = " + numberOfContours);
//        System.print.println("\t\tx " + xMin + ", " + xMax);
//        System.print.println("\t\ty " + yMin + ", " + yMax);
//        System.print.println(md5);
        MD5s[i] = md5;

      }

    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  public void parseLOCA(byte[] data) {
    try {
      locaOffset = new int[segCount];
      for (int i = 0; i < segCount; i++) {
        int offset = toInt(sub(data, i * 2, i * 2 + 1));
        locaOffset[i] = offset;
//        System.print.println(offset);
      }

    } catch (Exception e) {
      e.printStackTrace();
    }
  }


  public int getGlyphId(int characterId) {

    for (int i = 0; i < endCount.length; i++) {
      if (characterId <= endCount[i] && characterId >= startCount[i]) {
        return (characterId + isDealte[i]) % 65536;
      }
    }
    return -1;
  }

  public String getMD5(int characterId) {

    int GlyphId = getGlyphId(characterId);
//    System.print.println(GlyphId);
    if (GlyphId < segCount) {
      return MD5s[GlyphId];
    }
    return null;
  }

  public void parseMAXP(byte[] data) {
    for (byte b : data) {
      System.out.println(b);
    }
  }


  /**
   * characterID 到实际id的关联
   */
  private void parseCMAP(byte[] data) {
//    System.print.println("table data size = " + data.length);
    int start = toInt(sub(data, 10, 11));
    int format = toInt(sub(data, start, start + 1));
    int length = toInt(sub(data, start + 2, start + 3));
    int language = toInt(sub(data, start + 4, start + 5));
    segCount = toInt(sub(data, start + 6, start + 7)) / 2;
    int searchRange = toInt(sub(data, start + 8, start + 9));
    int entrySelector = toInt(sub(data, start + 10, start + 11));
    int rangeShift = toInt(sub(data, start + 12, start + 13));

    endCount = new int[segCount];
    startCount = new int[segCount];
    isDealte = new int[segCount];
    idRangeOffset = new int[segCount];

    for (int i = 0; i < segCount; i++) {
      endCount[i] = toInt(sub(data, start + 14 + 2 * i, start + 14 + 2 * i + 1));
      startCount[i] = toInt(sub(data, start + 14 + 2 * segCount + 2 + 2 * i,
          start + 14 + 2 * segCount + 2 + 2 * i + 1));
      isDealte[i] = toShort(sub(data, start + 14 + 4 * segCount + 2 + 2 * i,
          start + 14 + 4 * segCount + 2 + 2 * i + 1));
      idRangeOffset[i] = toShort(sub(data, start + 14 + 6 * segCount + 2 + 2 * i,
          start + 14 + 6 * segCount + 2 + 2 * i + 1));
    }
  }

  public byte[] loadBASE64(String fileName) {
    String line = IReader.cat(fileName).trim();
    byte[] bs = Base64.decodeBase64(line);
    return bs;
  }

  public byte[] loadWoffFile(String fileName) {
    try {
      return IOUtils.toByteArray(new FileReader(fileName));
    } catch (Exception e) {
      e.printStackTrace();
    }
    return null;
  }

  public Map<String, String> tag2md5(byte[] data) {
    byte[] head = sub(data, 0, 44);
    printHead(head);
    int numTables = numTables(head);
    System.out.println(numTables);
    numTables = 1000;
    byte[] tableDirectory = sub(data, 44, 44 + 20 * numTables);
    Map<String, String> result = parseTableDirectory(numTables, tableDirectory);
    return result;
  }


  private int numTables(byte[] head) {
    return toInt(sub(head, 12, 14));
  }

  private void printHead(byte[] head) {
    System.out.println("signature:\t" + toStr(sub(head, 0, 4)));
    System.out.println("flavor\t" + toStr(sub(head, 4, 8)));
    System.out.println("length\t" + toInt(sub(head, 8, 12)));
    System.out.println("numTables\t" + toInt(sub(head, 12, 14)));
    System.out.println("reserved\t" + toStr(sub(head, 14, 16)));
    System.out.println("totalSfntSize\t" + toInt(sub(head, 16, 20)));
    System.out.println("majorVersion\t" + toInt(sub(head, 20, 22)));
    System.out.println("minorVersion\t" + toInt(sub(head, 22, 24)));
    System.out.println("metaOffset\t" + toInt(sub(head, 24, 28)));
    System.out.println("metaLength\t" + toInt(sub(head, 28, 32)));
    System.out.println("metaOrigLength\t" + toInt(sub(head, 32, 36)));
    System.out.println("privOffset\t" + toInt(sub(head, 36, 40)));
    System.out.println("privLength\t" + toInt(sub(head, 40, 44)));
  }

  private Map<String, String> parseTableDirectory(int numTables, byte[] tableDirectory) {
    Map<String, String> result = new HashMap<>();
    for (int i = 0; i < numTables; i++) {
      String tag = toStr(sub(tableDirectory, i * 20, i * 20 + 4));
      String offset = toStr(sub(tableDirectory, i * 20 + 4, i * 20 + 8));
      String compLength = toStr(sub(tableDirectory, i * 20 + 8, i * 20 + 12));
      String origLength = toStr(sub(tableDirectory, i * 20 + 12, i * 20 + 16));
      String origChecksum = toStr(sub(tableDirectory, i * 20 + 16, i * 20 + 20));
      System.out.println(tag);
      System.out.println(offset);
      System.out.println(compLength);
      System.out.println(origLength);
      System.out.println(origChecksum);
      result.put(tag, origChecksum);
    }
    return result;
  }

  private static final char[] cs = new char[]{'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',
      'B', 'C', 'D', 'E', 'F'};

  private static String toStr(byte[] bs) {
    StringBuilder sb = new StringBuilder();
    for (byte b : bs) {
      sb.append(cs[(b >> 4) & 0xF]);
      sb.append(cs[b & 0xF]);
    }
    return sb.toString();
  }


  private static short toShort(byte[] bs) {
    return (short) toInt(bs);
  }

  private static int toInt(byte[] bs) {
    int v = 0;
    for (byte b : bs) {
      v = (v << 8) + (b & 0xFF);
    }
    return v;
  }


  private static long toLong(byte[] bs) {
    long v = 0;
    for (byte b : bs) {
      v = ((v << 8) + (b & 0xFF));
    }
    return v;
  }


  private static byte[] sub(byte[] bs, int start, int end) {
    byte[] result = new byte[end - start + 1];
    for (int i = 0; i < result.length; i++) {
      result[i] = bs[start + i];
    }
    return result;
  }

  private int tr(char c) {
    if (c >= 'A' && c <= 'Z') {
      return c - 'A';
    }
    if (c >= 'a' && c <= 'z') {
      return c - 'a' + 26;
    }
    if (c >= '0' && c <= '9') {
      return c - '0' + 52;
    }
    if (c == '+') {
      return 62;
    }
    if (c == '/') {
      return 63;
    }
    return -1;
  }

}
